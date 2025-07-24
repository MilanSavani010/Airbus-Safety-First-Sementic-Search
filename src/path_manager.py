from config import RAW_DIR, INDEXES_PATH, METADATAMAPS_PATH
from pathlib import Path


def ensure_directories_exist():
    paths = [RAW_DIR, INDEXES_PATH, METADATAMAPS_PATH]

    for path in paths:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {path}")
        else:
            print(f"✅Directory exists: {path}")