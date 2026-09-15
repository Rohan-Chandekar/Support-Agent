import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

DOCS_DIR = "data/product_docs"

def build_product_docs_store():
    docs = []
    for filename in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, filename)
        loader = TextLoader(path)
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    store = FAISS.from_documents(chunks, embeddings)
    return store

_product_docs_store = build_product_docs_store()

def retrieve_product_docs(query: str, k: int = 2) -> list[str]:
    results = _product_docs_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]