from pathlib import Path
import fitz  # PyMuPDF
import re

# Chemins relatifs depuis la racine du dépôt
INPUT_PATH = Path("data/raw/POWER - Les 48 lois de pouvoir - Robert Greene.pdf")
OUTPUT_PATH = Path("data/clean/book_cleaned.txt")

# Vérification du fichier PDF
if not INPUT_PATH.exists():
    raise FileNotFoundError(f"PDF introuvable : {INPUT_PATH}. Vérifiez le chemin ou téléversez le fichier.")

def extract_text_from_pdf(pdf_path):
    """Extrait le texte du PDF avec PyMuPDF."""
    doc = fitz.open(pdf_path)
    return "".join([page.get_text("text") for page in doc])

def clean_text(text):
    """Nettoie le texte extrait."""
    text = re.sub(r'\n', ' ', text)  # Retours à la ligne → espaces
    text = re.sub(r'\s{2,}', ' ', text)  # Espaces multiples → simple
    text = re.sub(r'Page \d+', '', text)  # Supprime les numéros de page
    return text.strip()

if __name__ == "__main__":
    print("Début de l'extraction...")
    raw_text = extract_text_from_pdf(INPUT_PATH)
    cleaned_text = clean_text(raw_text)
    
    # Crée le dossier de sortie si nécessaire
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarde le texte nettoyé
    OUTPUT_PATH.write_text(cleaned_text, encoding="utf-8")
    print(f"✅ Texte nettoyé sauvegardé dans : {OUTPUT_PATH}")
