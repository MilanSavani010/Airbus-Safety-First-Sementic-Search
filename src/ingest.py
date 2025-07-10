"""
pdf_ingest.py  ─  Load PDF pages into the staging table.

• For every *.pdf in data/raw/:
    1. Use pdfminer to extract embedded text.
    2. If embedded text length < 40 chars,
       render that page to PNG and OCR via EasyOCR.
• Store (file_name, page_number, extracted_text) in staging_pdf.
"""

from pathlib import Path
import sqlite3

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import cv2
import torch
import easyocr

from src.config import RAW_DIR, DB_PATH

# EasyOCR reader (GPU if available)
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())


def ocr_image(img):
    """OCR a PIL image using EasyOCR and return plain text."""
    # pdf2image returns PIL — convert to OpenCV BGR
    import numpy as np
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = reader.readtext(img_bgr, detail=0)  # list of strings
    return " ".join(result).strip()


def process_pdf(pdf_path: Path) -> list[tuple[str, int, str]]:
    """Return list of (file, page, text) rows for staging."""
    rows = []
    try:
        embedded = extract_text(pdf_path, laparams=None)
    except Exception as exc:
        print(f"[PDF] {pdf_path.name}: pdfminer error → {exc}")
        embedded = ""

    # Split embedded text by page delimiter \f inserted by pdfminer
    pages_embedded = embedded.split("\f")

    # Ensure renderable list of PIL images (one per page)
    images = convert_from_path(pdf_path, dpi=300)

    for idx, pil_img in enumerate(images, start=1):
        text = pages_embedded[idx - 1].strip() if idx - 1 < len(pages_embedded) else ""

        # Fallback to OCR when embedded text looks empty
        if len(text) < 40:  # heuristic threshold
            text = ocr_image(pil_img)

        rows.append((pdf_path.name, idx, text))
    return rows


def main() -> None:
    pdf_files = sorted(p for p in RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files in data/raw/")
        return

    all_rows: list[tuple[str, int, str]] = []
    for pdf in pdf_files:
        rows = process_pdf(pdf)
        all_rows.extend(rows)
        print(f"[PDF] {pdf.name}: {len(rows)} pages processed")

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.executescript(
            """
            DROP TABLE IF EXISTS staging_pdf;
            CREATE TABLE staging_pdf (
              fname TEXT,
              page  INTEGER,
              text  TEXT,
              PRIMARY KEY (fname, page)
            );
            """
        )
        cur.executemany("INSERT INTO staging_pdf VALUES (?, ?, ?)", all_rows)
        con.commit()

    print(f"[PDF] Loaded {len(all_rows)} pages into staging_pdf ({DB_PATH})")


if __name__ == "__main__":
    main()
