from sentence_transformers import SentenceTransformer
import fitz 
from bd_settings import client
embedder = SentenceTransformer("intfloat/multilingual-e5-large")

def load_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)

def chunk(text, size=500, overlap=100):
    """Чанкинг с перекрытием; для русского текста 300–700 токенов — рабочий диапазон."""
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i + size])

text = load_pdf("docs/Заказ еды из столовой Системная аналитика.pdf")
points = []
for i, ch in enumerate(chunk(text)):
    vec = embedder.encode("passage: " + ch, normalize_embeddings=True)
    points.append({"id": i, "vector": vec.tolist(),
                   "payload": {"text": ch, "source": "Заказ еды из столовой Системная аналитика.pdf"}})

client.upsert(collection_name="docs", points=points)