                              ┌──────────────┐
                    START ──► │  preprocess  │  clean text, extract email
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │   classify   │  category + priority (LLM, structured output)
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │  rag_docs    │  retrieve product docs (FAISS)
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │ rag_tickets  │  retrieve similar past tickets (FAISS)
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │     sla      │  custom tool: SLA deadline calc
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │   generate   │  draft reply grounded in RAG context (LLM)
                              └──────┬───────┘
                                     ▼
                              ┌──────────────┐
                              │   validate   │  confidence score (LLM, structured output)
                              └──────┬───────┘
                                     ▼
                          [conditional edge: confidence ≥ 0.7?]
                                     │
                     ┌───────────────┴────────────────┐
                    YES                                NO
                     ▼                                  ▼
            ┌────────────────┐                ┌──────────────────┐
            │  format_reply  │                │     escalate      │
            │ (success path) │                │ (fallback path,   │
            │                │                │  MCP tool call)   │
            └───────┬────────┘                └─────────┬─────────┘
                     ▼                                    ▼
                    END                                  END


# Customer Support Ticket Resolution Agent

An agentic support-ticket triage system built with LangGraph. It classifies
incoming tickets, retrieves grounding context from two knowledge sources,
drafts a reply, and — based on a confidence check — either auto-resolves
the ticket or escalates it to a human via an MCP tool call.

## Architecture

See `docs/architecture.txt` for the full diagram. Summary of the 9 nodes:

| Node          | Type              | Purpose |
|---------------|-------------------|---------|
| preprocess    | deterministic     | clean ticket text, extract customer email |
| classify      | LLM (structured)  | assign category + priority |
| rag_docs      | RAG               | retrieve relevant product documentation |
| rag_tickets   | RAG               | retrieve similar past resolved tickets |
| sla           | custom tool       | compute SLA deadline from category/priority |
| generate      | LLM               | draft a grounded customer reply |
| validate      | LLM (structured)  | score confidence that the reply is safe to send |
| format_reply  | deterministic     | finalize reply for the success path |
| escalate      | MCP tool call     | create a human-review escalation on the fallback path |

**Conditional edge:** after `validate`, if `confidence >= 0.7` the graph
routes to `format_reply` (auto-resolve). Otherwise it routes to `escalate`
(human review via MCP).

## Setup

1. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Create `.env` with `OPENAI_API_KEY=your_key_here`

## Running

```bash
python -m src.main
```

This runs a sample ticket through the full graph and prints the final state.
Edit `src/main.py` to test different ticket text.

## Execution flow

1. Raw ticket text enters as `TicketState`.
2. Each node reads specific state fields and returns a partial update,
   which LangGraph merges into the running state.
3. State accumulates: by the `validate` node, it contains classification,
   two sets of retrieved context, SLA info, and a draft reply.
4. The conditional edge inspects `confidence` and routes to one of two
   terminal nodes.
5. Both terminal nodes write `final_reply` and `escalated`, so any run's
   outcome can be read directly from final state.

## Design decisions

- **Two separate RAG sources** (product docs vs. past tickets) instead of
  one merged store — they answer different questions (policy fact vs.
  precedent/resolution) and merging would blur retrieval relevance.
- **Structured LLM output** (Pydantic schemas via `with_structured_output`)
  for classification and confidence scoring, instead of free-text parsing —
  removes an entire class of parsing failures.
- **Confidence scored by a separate LLM call**, not self-reported by the
  generation node — a dedicated "judge" call is more reliable than trusting
  a model to accurately grade its own output in the same turn.
- **SLA logic is a plain deterministic function**, not an LLM call — it's a
  business rule that must be consistent and unit-testable, not "creative."
- **Escalation goes through MCP** rather than a direct function call, so the
  node code is decoupled from the actual ticketing backend — swapping the
  simulated JSON-file backend for a real system (Zendesk, Jira) requires no
  changes to the graph.

## Production improvements (not implemented here, but noted)

- Run `rag_docs` and `rag_tickets` in parallel (fan-out/fan-in) since they
  don't depend on each other's output.
- Replace in-memory FAISS with a persistent vector store (Pinecone, pgvector)
  and an incremental re-indexing pipeline instead of rebuilding on startup.
- Add retry/timeout handling around all LLM and MCP calls.
- Add structured logging/tracing (e.g. LangSmith) for observability across
  every node, not just print statements.
- Point the MCP escalation server at a real ticketing system's API instead
  of a local JSON file.
- Add authentication/rate limiting if this were exposed as a service.