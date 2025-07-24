from importlib.metadata import metadata

import pymupdf4llm
from markdown import markdown
from bs4 import BeautifulSoup
import re
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer('all-MiniLM-L6-v2')

def md_to_plain_text(md_text):
    html = markdown(md_text)
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text(separator="\n")


def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # whitespace normalization
    text = re.sub(r"[^a-zA-Z0-9,.!? ]", "", text)  # remove punctuation symbols
    return text.strip()

def word_level_chunking(text, max_words=150):
    words = clean_text(text).split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks



page_chunks = pymupdf4llm.to_markdown('../data/raw/safety_first_34.pdf',write_images=False,page_chunks=True)

chunked_pages = []

for page_chunk in page_chunks:
    text = md_to_plain_text(page_chunk['text'])
    cleaned = clean_text(page_chunk['text'])
    chuncked_texts = word_level_chunking(cleaned,max_words=10)

    for chunk_text in chuncked_texts:
        chunked_pages.append( {
            "page":page_chunk['metadata']['page'],
            "filepath":page_chunk['metadata']['file_path'],
            "plain_text":chunk_text,
        })

texts = [chunk['plain_text'] for chunk in chunked_pages]
embeddings = model.encode(texts,show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

#number of chuncks
#print(embeddings.shape[0])

#index position to connect each vector to its corresponding metadata
#print(embeddings.shape[1])

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
print(index)
metadata_map = {
    i: {
        "page": chunked_pages[i]['page'],
        "filepath":chunked_pages[i]['filepath'],
        "text":chunked_pages[i]['plain_text']
    } for i in range(len(chunked_pages))
}

query = "Microbiological contamination"
query_embed = model.encode([query]).astype("float32")
D, I = index.search(query_embed, k=50)

for idx in I[0]:
    match = metadata_map[idx]
    print(f"\nMatch Found:")
    print(f"File: {match['filepath']} | Page: {match['page']}")
    print(match["text"])
