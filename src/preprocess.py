import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w.,!? ]+", "", text)
    return text.strip()

def word_level_chunking(text, max_words=150):
    words = clean_text(text).split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def prepare_chunks(raw_chunks):
    processed = []
    for chunk in raw_chunks:
        page = chunk['metadata']['page']
        filepath = chunk['metadata']['filepath']
        chunks = word_level_chunking(chunk['text'])
        for c in chunks:
            processed.append({
                "page": page,
                "filepath": filepath,
                "plain_text": c
            })
    return processed