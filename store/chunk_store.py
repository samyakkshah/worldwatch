from typing import Dict, List
from models.chunk import Chunk


class ChunkStore:
    def __init__(self):
        self.store: Dict[str, Chunk] = {}

    def add(self, chunk: Chunk):
        self.store[chunk.chunk_id] = chunk
    
    def get(self, chunk_id:str):
        return self.store[chunk_id] if self.exists(chunk_id) else None
    
    def get_by_article(self, article_id:str) -> List[Chunk]:
        all_chunks = []
        for chunk in self.store.values():
            if chunk.article_id == article_id:
                all_chunks.append(chunk)
        return all_chunks
    
    def get_by_narrative(self, narrative_id: str) -> List[Chunk]:
        all_chunks = []
        for chunk in self.store.values():
            if chunk.narrative_id == narrative_id:
                all_chunks.append(chunk)
        return all_chunks
    
    def get_top_k_chunks(self, chunk: Chunk, k:int = 10, threshold:float = 0.5):
        import heapq
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        top_matching_chunks = []
        for old_chunk in self.store.values():
            cos_sim = cosine_similarity(
                np.array([chunk.embedding]), 
                np.array([old_chunk.embedding])
            )[0][0]
            if cos_sim>threshold:
                top_matching_chunks.append( (cos_sim, old_chunk.narrative_id))
        if not top_matching_chunks:
            return []
        
        heapq.heapify(top_matching_chunks)
        
        res = heapq.nlargest(k, top_matching_chunks, key=lambda x: x[0])
        return res

    def to_dict(self):
        def serialize(obj):
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(v) for v in obj]
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            else:
                return obj

        return {
            cid: {k: serialize(v) for k, v in vars(chunk).items()}
            for cid, chunk in self.store.items()
        }
    
    def save(self, path='chunk_store.json'):
        import json

        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load(self, path='chunk_store.json'):
        import json
        import os

        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
            
            for cid, chunk_data in data.items():
                self.store[cid] = Chunk.from_dict(chunk_data)
        else:
            self.store = {}

    def update(self, chunk_id: str, **fields):
        chunk = self.get(chunk_id)
        if not chunk:
            return False
        for field, value in fields.items():
            if hasattr(chunk, field):
                setattr(chunk, field, value)
        return True
            

    def exists(self, chunk_id:str):
        return chunk_id in self.store
    