import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

TICKETS_DIR = "data/past_tickets"

def build_past_tickets_store():
    docs = []
    for filename in os.listdir(TICKETS_DIR):
        path = os.path.join(TICKETS_DIR, filename)
        loader = TextLoader(path)
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    store = FAISS.from_documents(chunks, embeddings)
    return store

_past_tickets_store = build_past_tickets_store()

def retrieve_past_tickets(query: str, k: int = 2) -> list[str]:
    results = _past_tickets_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]