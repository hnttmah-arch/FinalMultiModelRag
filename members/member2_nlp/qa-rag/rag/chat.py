from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama


# ==========================
# LOAD EMBEDDING MODEL
# ==========================

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================
# LOAD VECTOR DATABASE
# ==========================

db = Chroma(
    persist_directory="./vectordb",
    embedding_function=embedding
)


# TEST VECTOR DB
print("\nLoading Vector DB...")

try:
    total = db._collection.count()
    print(f"Loaded chunks: {total}")
except Exception as e:
    print("Vector DB error:", e)


retriever = db.as_retriever(
    search_kwargs={"k": 3}
)


# ==========================
# CHAT LOOP
# ==========================

while True:

    question = input("\nAsk BMW > ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    print(f"\nRetrieved: {len(docs)} chunks")

    if len(docs) == 0:
        print("\nNo document found\n")
        continue

    context = "\n\n".join([
        d.page_content
        for d in docs
    ])

    print("\n===== RETRIEVED =====")
    print(context[:3000])
    print("\n=====================\n")

    prompt = f"""
You are BMW Assistant.

RULES:
- Use ONLY context
- Never invent information
- If not found say:
I cannot find information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nBMW BOT:\n")
    print(
        response["message"]["content"]
    )