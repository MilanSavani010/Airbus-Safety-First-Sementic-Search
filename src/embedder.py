from sentence_transformers import SentenceTransformer
import numpy as np
from config import EMBEDDING_MODEL_NAME
from logger import get_logger

logger = get_logger("embedder")

def embed_chunks(chunk_list, model_name=EMBEDDING_MODEL_NAME):
    model = SentenceTransformer(model_name)
    texts = [c["plain_text"] for c in chunk_list]

    metadata = [{
        "page": c["page"],
        "filepath": c["filepath"],
        "text": c["plain_text"]
    } for c in chunk_list]

    embeddings = model.encode(texts, show_progress_bar=True)
    logger.info(f"Embedded {len(texts)} chunks")
    return np.array(embeddings).astype("float32"), metadata