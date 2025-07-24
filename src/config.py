from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT_DIR / "data" / "raw"
INDEXES_PATH = ROOT_DIR / "output" / "indexes"
METADATAMAPS_PATH = ROOT_DIR / "output" / "metadatamaps"

BATCH_SIZE = 2  # PDFs per batch

CHUNK_WORD_COUNT = 150  # Words per chunk

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # Based on model (MiniLM = 384)

LOG_LEVEL = "INFO"