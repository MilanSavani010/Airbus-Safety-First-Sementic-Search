import faiss
import json
from config import EMBEDDING_DIMENSION
from logger import get_logger

logger = get_logger("indexer")

def save_index(embeddings, index_file_path):
    index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
    index.add(embeddings)
    faiss.write_index(index, str(index_file_path))
    logger.info(f"Saved index file: {index_file_path.name}")

def save_metadata(metadata, metadata_file_path):
    with open(metadata_file_path, "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved metadata file: {metadata_file_path.name}")