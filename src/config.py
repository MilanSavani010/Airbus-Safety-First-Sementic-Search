from pathlib import Path
import platform

ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT_DIR / "data" / "raw"       # where PDFs live
INDEXES_PATH = ROOT_DIR /"output"/ "indexes"        # index file
METADATAMAPS_PATH = ROOT_DIR /"output"/ "metadatapaths"

