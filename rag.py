from fastapi import FastAPI
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import uvicorn
from embedder_model import embedder
from bd_settings import client
app = FastAPI()
llm = OpenAI(base_url="http://localhost:8080/v1", api_key="local-key")


SYSTEM = """Ты — ассистент. Отвечай ТОЛЬКО на основе контекста ниже.
Если ответа нет в контексте — прямо скажи об этом.
Контекст:
{context}"""

@app.post("/ask")
def ask(question: str):
    q_vec = embedder.encode("query: " + question, normalize_embeddings=True).tolist()
    hits = client.query_points(collection_name="docs", query=q_vec, limit=5).points
    context = "\n\n".join(h.payload["text"] for h in hits)

    resp = llm.chat.completions.create(
        model="gigachat-local",
        messages=[
            {"role": "system", "content": SYSTEM.format(context=context)},
            {"role": "user", "content": question},
        ],
        temperature=0.1,
    )
    return {"answer": resp.choices[0].message.content,
            "sources": [h.payload["source"] for h in hits]}

# uvicorn rag:app --host 0.0.0.0 --port 8000