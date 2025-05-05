
from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import chromadb  # Base de données vectorielle
from chromadb.config import Settings

# --- Configuration des chemins ---
CHUNKS_PATH = Path("data/chunks/chunks.json")  # Fichier des chunks texte
CHROMA_DB_DIR = "data/chroma_db"  # Dossier pour la base ChromaDB

# --- Modèle d'embedding ---
model = SentenceTransformer('all-MiniLM-L6-v2')  

# --- Chargement des chunks ---
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]
ids = [str(i) for i in range(len(texts))]  # IDs uniques pour chaque chunk

# --- Génération des embeddings ---
embeddings = model.encode(texts, show_progress_bar=True)

# --- Initialisation de ChromaDB ---
chroma_client = chromadb.Client(Settings(
    persist_directory=CHROMA_DB_DIR,  # Stockage persistant sur disque
    is_persistent=True
))

# Création ou récupération de la collection
collection = chroma_client.create_collection(
    name="text_chunks",  # Nom de la collection
    metadata={"hnsw:space": "cosine"}  # Similarité cosinus (par défaut)
)

# --- Ajout des données à ChromaDB ---
collection.add(
    documents=texts,          # Textes originaux
    embeddings=embeddings.tolist(),  # Converti en liste (format attendu)
    ids=ids                   # Identifiants uniques
)

# --- Sauvegarde persistante ---
chroma_client.persist()

print(f"✅ {len(texts)} chunks stockés dans ChromaDB (dossier: {CHROMA_DB_DIR})")
