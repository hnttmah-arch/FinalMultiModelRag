from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = "data"

all_docs = []

pdfs = Path(DATA_DIR).glob("*.pdf")

for pdf in pdfs:
    loader = PyPDFLoader(str(pdf))

    docs = loader.load()

    all_docs.extend(docs)

print("Total pages:", len(all_docs))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = splitter.split_documents(
    all_docs
)

print("Total chunks:", len(chunks))

print("\n=== SAMPLE ===\n")

print(
    chunks[0].page_content[:500]
)