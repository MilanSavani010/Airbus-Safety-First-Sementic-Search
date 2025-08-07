from path_manager import ensure_directories_exist
from batch_processor import get_pdf_batches, process_batch
from logger import get_logger

logger = get_logger("main")

def run_batch_pipeline():
    logger.info("Starting PDF indexing pipeline...")
    ensure_directories_exist()

    for batch_id, pdf_batch in enumerate(get_pdf_batches(), start=1):
        process_batch(pdf_batch, batch_id)

    logger.info("Pipeline complete. All batches processed.")

if __name__ == "__main__":
    run_batch_pipeline()
    pass