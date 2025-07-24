import shutil
from pathlib import Path

# Source: where your PDFs already live
RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# Destination: where Streamlit dashboard expects static files
STATIC_PDF_DIR = Path(__file__).parent / "static" / "pdfs"

def sync_pdfs():
    STATIC_PDF_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    for pdf_file in RAW_DIR.glob("*.pdf"):
        dest_file = STATIC_PDF_DIR / pdf_file.name
        shutil.copyfile(pdf_file, dest_file)
        count += 1

    print(f"Synced {count} PDFs to: {STATIC_PDF_DIR}")

if __name__ == "__main__":
    sync_pdfs()