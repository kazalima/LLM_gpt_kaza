from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json
from pathlib import Path

# Configuration
CHUNKS_PATH = Path("data/chunks/chunks.json")
CHROMA_DB_DIR = "data/chroma_db"

# Modèle d'embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Charger les chunks
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]
ids = [str(i) for i in range(len(texts))]

# Générer les embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Client ChromaDB - Version corrigée
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)  # Changement ici

collection = chroma_client.get_or_create_collection(
    name="text_chunks",
    metadata={"hnsw:space": "cosine"}
)

# Ajout des données
collection.add(
    documents=texts,
    embeddings=embeddings.tolist(),
    ids=ids
)

print(f"✅ {len(texts)} embeddings stockés dans ChromaDB")
