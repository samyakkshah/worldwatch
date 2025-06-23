from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from models.chunk import Chunk

class Narrative:
    def __init__(self, chunks: List[Chunk], article_id):
        self.narrative_id = str(uuid4())
        self.title = "pending"
        self.tldr_summary = "pending"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.last_updated_at = datetime.now(timezone.utc).isoformat()
        self.source_article_ids = set(article_id)
        self.chunks = [chunk.chunk_id for chunk in chunks]
        self.heat_score = 1
        self.view_points = "pending"
        
        sentiment_scores = [chunk.sentiment for chunk in chunks]
        self.sentiment_trend = sum(sentiment_scores)/len(sentiment_scores)

        self.topic = "pending"
        self.decay = 3
    
    def update(self, chunks: List[Chunk], article_id):
        self.source_article_ids.add(article_id)
        self.chunks.extend([chunk.chunk_id for chunk in chunks])

        sentiment_scores = [chunk.sentiment for chunk in chunks]
        self.sentiment_trend = (self.sentiment_trend + sum(sentiment_scores)/len(sentiment_scores))/2
        self.heat_score +=1
        self.decay+=3
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj