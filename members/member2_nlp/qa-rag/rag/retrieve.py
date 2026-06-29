from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./vectordb",
    embedding_function=embedding
)

query = "What is the fuel tank capacity of BMW XM?"

docs = db.similarity_search(query, k=3)

for i, doc in enumerate(docs):
    print(f"\n=== RESULT {i+1} ===")
    print(doc.page_content[:1000])