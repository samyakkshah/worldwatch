import nltk
from sentence_transformers import SentenceTransformer, util
import numpy as np
from textblob import TextBlob

nltk.download('punkt')

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_chunking(text, max_tokens):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = []
    token_count = 0
    idx = 0

    for sentence in sentences:
        sentence_tokens = sentence.split()
        if token_count + len(sentence_tokens) <= max_tokens:
            current_chunk.append(sentence)
            token_count += len(sentence_tokens)
        else:
            if current_chunk:
                chunk_text = " ".join(current_chunk)
                embedding = embedder.encode(chunk_text)
                sentiment = TextBlob(chunk_text).sentiment.polarity # type: ignore
                chunks.append({
                    "idx": idx,
                    "body": chunk_text,
                    "embedding": embedding,
                    "sentiment": sentiment
                })
                idx += 1
            current_chunk = [sentence]
            token_count = len(sentence_tokens)

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        embedding = embedder.encode(chunk_text)
        sentiment = TextBlob(chunk_text).sentiment.polarity # type: ignore
        chunks.append({
            "idx": idx,
            "body": chunk_text,
            "embedding": embedding,
            "sentiment": sentiment
        })

    return chunks