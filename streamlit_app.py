import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.graph import build_graph

st.set_page_config(page_title="Support Ticket Agent", page_icon="🎫")
st.title("🎫 Customer Support Ticket Resolution Agent")
st.caption("LangGraph agent: classifies, retrieves context, drafts a reply, and auto-resolves or escalates.")

# Build the graph once per session, not on every click
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

ticket_text = st.text_area(
    "Paste a customer ticket:",
    height=120,
    placeholder="e.g. Hi, I was charged twice this month. My email is jane@example.com",
)

if st.button("Run Agent", type="primary"):
    if not ticket_text.strip():
        st.warning("Please enter a ticket first.")
    else:
        with st.spinner("Running through the graph..."):
            result = st.session_state.graph.invoke({"raw_ticket": ticket_text})

        st.divider()

        col1, col2, col3 = st.columns(3)
        col1.metric("Category", result.get("category", "—"))
        col2.metric("Priority", result.get("priority", "—"))
        col3.metric("Confidence", f"{result.get('confidence', 0):.2f}")

        st.divider()

        if result.get("escalated"):
            st.error("🚨 Escalated to human review")
            st.write(f"**Reason:** Low confidence score ({result.get('confidence')})")
            st.write("An escalation ticket was created via MCP. See `mcp_server/escalations.json`.")
            with st.expander("View AI's draft reply (for reviewer reference)"):
                st.write(result.get("draft_reply", ""))
        else:
            st.success("✅ Auto-resolved")
            st.write("**Final reply sent to customer:**")
            st.write(result.get("final_reply", ""))

        with st.expander("View full internal state (debug)"):
            st.json(result)