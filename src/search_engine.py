import faiss
import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from config import INDEXES_PATH, METADATAMAPS_PATH, EMBEDDING_MODEL_NAME
from logger import get_logger

logger = get_logger("search_engine")

# Load embedding model once
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def load_faiss_index(index_path: Path):
    index = faiss.read_index(str(index_path))
    logger.info(f"Loaded FAISS index from: {index_path.name}")
    return index

def load_metadata(metadata_path: Path):
    with open(metadata_path) as f:
        metadata = json.load(f)
    logger.info(f"Loaded metadata map from: {metadata_path.name}")
    return metadata

def search_query_across_batches(query: str, top_k: int = 5):
    query_vector = model.encode([query]).astype("float32")
    all_results = []

    # Pair all .index and .json files by batch ID
    index_files = sorted(INDEXES_PATH.glob("*.index"))
    for index_file in index_files:
        batch_id = index_file.stem.split("_")[-1]
        metadata_file = METADATAMAPS_PATH / f"safety_batch_{batch_id}.json"

        # Safety: ensure metadata exists
        if not metadata_file.exists():
            logger.warning(f"Missing metadata for batch {batch_id}")
            continue

        # Load index + metadata
        index = load_faiss_index(index_file)
        metadata = load_metadata(metadata_file)

        # Run FAISS search
        D, I = index.search(query_vector, top_k)

        for rank, idx in enumerate(I[0]):
            if idx >= len(metadata):
                logger.warning(f"Invalid metadata index: {idx} in batch {batch_id}")
                continue

            result = {
                "page": metadata[idx]["page"],
                "filepath": metadata[idx]["filepath"].split("/")[-1],
                "text": metadata[idx]["text"],
                "batch": batch_id,
                "distance": float(D[0][rank]),
                "rank": rank + 1
            }
            all_results.append(result)

    # Sort globally by lowest distance (most relevant)
    all_results.sort(key=lambda x: x["distance"])
    return all_results[:top_k]