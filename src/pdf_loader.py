from pymupdf4llm import to_markdown
from logger import get_logger

logger = get_logger("pdf_loader")


def load_pdf_chunks_from_files(pdf_paths):
    all_chunks = []

    for pdf_path in pdf_paths:
        chunks = to_markdown(str(pdf_path), page_chunks=True)
        logger.info(f"Loaded {len(chunks)} chunks from {pdf_path.name}")

        for chunk in chunks:
            chunk['metadata']['filepath'] = str(pdf_path)
            all_chunks.append(chunk)

    return all_chunks