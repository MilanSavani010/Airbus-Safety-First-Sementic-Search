from config import RAW_DIR, INDEXES_PATH, METADATAMAPS_PATH, BATCH_SIZE
from pdf_loader import load_pdf_chunks_from_files
from preprocess import prepare_chunks
from embedder import embed_chunks
from indexer import save_index, save_metadata
from logger import get_logger

logger = get_logger("batch_processor")

def get_pdf_batches(batch_size=BATCH_SIZE):
    pdf_files = sorted(RAW_DIR.glob("*.pdf"))
    for i in range(0, len(pdf_files), batch_size):
        yield pdf_files[i:i + batch_size]

def process_batch(batch_files, batch_id):
    logger.info(f"Batch {batch_id} — {len(batch_files)} PDFs")

    raw_chunks = load_pdf_chunks_from_files(batch_files)
    processed_chunks = prepare_chunks(raw_chunks)
    embeddings, metadata = embed_chunks(processed_chunks)

    index_path = INDEXES_PATH / f"safety_batch_{batch_id}.index"
    metadata_path = METADATAMAPS_PATH / f"safety_batch_{batch_id}.json"

    save_index(embeddings, index_path)
    save_metadata(metadata, metadata_path)

    logger.info(f"✅ Batch {batch_id} indexed: {index_path.name} & {metadata_path.name}")