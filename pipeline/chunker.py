from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document
import nltk
from sentence_transformers import SentenceTransformer
import numpy as np
import spacy
from textblob import TextBlob

from llama_index.core.schema import BaseNode
from typing import List

embedder = SentenceTransformer("all-MiniLM-L6-v2") 

def chunking(text: str, chunk_size:int= 100, chunk_overlap = 50):
    splitter = SentenceSplitter( chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = [Document(text=text)]
    nodes: List[BaseNode] = splitter.get_nodes_from_documents(documents)
    return nodes

nlp = spacy.load('en_core_web_sm')

def semantic_chunking(text, max_tokens=100):
    nodes: List[BaseNode] = chunking(text)
    chunks = []
    for idx, node in enumerate(nodes):
        body = node.get_content()
        sentiment = TextBlob(body).sentiment.polarity # type: ignore
        embedding = embedder.encode(body)
        topics = extract_entities_from_spacy(body)
        chunks.append({
            "idx": idx,
            "body": body,
            "embedding": embedding,
            "sentiment": sentiment,
            "topics": topics,
        })

    return chunks


def extract_entities_from_spacy(text:str):
    doc = nlp(text)
    topics = dict()
    for entity in doc.ents:
        if len(entity.text.strip())>2:
            if entity.label_.lower() not in topics:
                topics[(entity.label_).lower()] = set()
            topics[entity.label_.lower()].add(entity.text.strip())
    return topics