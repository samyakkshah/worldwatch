import nltk
from sentence_transformers import SentenceTransformer, util
import numpy as np
from textblob import TextBlob
from rake_nltk import Rake
rake = Rake()

def extract_keywords(text):
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:5]  # top 5 phrases

nltk.download('punkt')

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_chunking(text, max_tokens=100):
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.download('wordnet')
    lemmatizer = WordNetLemmatizer()

    def clean_text(text):
        words = word_tokenize(text)
        return " ".join([lemmatizer.lemmatize(w.lower()) for w in words if w.isalnum()])

    sentences = sent_tokenize(text)
    chunks, current_chunk, token_count, idx = [], [], 0, 0

    for sentence in sentences:
        tokens = sentence.split()
        if len(tokens) < 5: continue  # skip very short sentences
        if token_count + len(tokens) <= max_tokens:
            current_chunk.append(sentence)
            token_count += len(tokens)
        else:
            if current_chunk:
                body = " ".join(current_chunk)
                embedding = embedder.encode(clean_text(body))
                sentiment = TextBlob(body).sentiment.polarity  # type: ignore
                topics = extract_keywords(body)
                chunks.append({
                    "idx": idx,
                    "body": body,
                    "embedding": embedding,
                    "sentiment": sentiment,
                    "topics": topics
                })
                idx += 1
            current_chunk = [sentence]
            token_count = len(tokens)

    if current_chunk:
        body = " ".join(current_chunk)
        embedding = embedder.encode(clean_text(body))
        sentiment = TextBlob(body).sentiment.polarity  # type: ignore
        topics = extract_keywords(body)
        chunks.append({
            "idx": idx,
            "body": body,
            "embedding": embedding,
            "sentiment": sentiment,
            "topics": topics,
        })

    return chunks
