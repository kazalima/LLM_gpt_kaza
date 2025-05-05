import json
from pathlib import Path

INPUT_PATH = Path("data/clean/book_cleaned.txt")
OUTPUT_PATH = Path("data/chunks/chunks.json")

def chunk_text(text, max_words=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append({"id": i // max_words, "text": chunk})
    return chunks

if __name__ == "__main__":
    text = INPUT_PATH.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"✅ {len(chunks)} chunks sauvegardés dans : {OUTPUT_PATH}")
