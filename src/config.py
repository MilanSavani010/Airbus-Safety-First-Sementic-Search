from pathlib import Path

# --- Root of the repo -------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]

# --- I/O paths --------------------------------------------------------------
RAW_DIR = ROOT_DIR / "data" / "raw"       # where PDFs / images live
DB_PATH = ROOT_DIR /"db"/ "srm_demo.db"        # SQLite file

# --- OCR settings -----------------------------------------------------------
# On Windows, pdf2image needs the Poppler bin dir on PATH.
POPPLER_BIN = r"C:\ProgramData\chocolatey\lib\poppler\tools"
DPI = 300                                 # OCR-friendly resolution
