from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DATA_DIR = "data"


all_docs = []

pdfs = Path(DATA_DIR).glob("*.pdf")

for pdf in pdfs:

    loader = PyPDFLoader(
        str(pdf)
    )

    docs = loader.load()

    all_docs.extend(
        docs
    )


print(
    "Pages:",
    len(all_docs)
)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(
    all_docs
)


print(
    "Chunks:",
    len(chunks)
)


embedding = HuggingFaceEmbeddings(
    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)


db = Chroma.from_documents(
    chunks,
    embedding,
    persist_directory=
    "./vectordb"
)


print(
    "Vector DB created"
)