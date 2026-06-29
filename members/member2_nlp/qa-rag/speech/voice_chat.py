import whisper
import ollama

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


print("Loading STT...")
stt = whisper.load_model("base")

print("Loading Vector DB...")
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="vectordb",
    embedding_function=embedding
)

print("Loading LLM...")


while True:

    audio = input("\nAudio file (exit): ")

    if audio == "exit":
        break

    text = stt.transcribe(audio)["text"]

    print("\nQuestion:")
    print(text)

    docs = db.similarity_search(text, k=3)

    context = "\n\n".join([
        d.page_content
        for d in docs
    ])

    prompt = f"""
Context:
{context}

Question:
{text}

Answer only from context.
"""

    res = ollama.chat(
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
        res["message"]["content"]
    )