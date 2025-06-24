from datetime import datetime, timezone
from typing import List, Optional, Set
from uuid import uuid4
from models.chunk import Chunk

class Narrative():
    def __init__(self, chunks: List[Chunk], article_source:str, article_id: str, article_image: Optional[str]):
        self.narrative_id = str(uuid4())
        self.title: str = ""
        self.summary = "pending"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.last_updated_at = datetime.now(timezone.utc).isoformat()
        self.source_article_ids = [article_id]
        self.sources = [article_source]
        self.chunks = [chunk.chunk_id for chunk in chunks]
        self.heat_score = 1
        self.view_points = "pending"
        self.images: Set[str] = set([article_image]) if article_image else set()
        self.story_text: str = ''
        sentiment_scores = [chunk.sentiment for chunk in chunks]
        self.sentiment_trend = sum(sentiment_scores)/len(sentiment_scores)
        
        self.topic = "pending"
        self.decay = 3
        self.report: str = ''
    
    def update(self, chunks: List[Chunk],  article_source:str, article_id: str, article_image:Optional[str]=None):
        self.source_article_ids.append(article_id)
        existing = set(self.chunks)
        incoming = {chunk.chunk_id for chunk in chunks}
        self.chunks = list(existing.union(incoming))
        self.sources.append(article_source)
        sentiment_scores = [chunk.sentiment for chunk in chunks]
        self.sentiment_trend = (self.sentiment_trend + sum(sentiment_scores)/len(sentiment_scores))/2
        self.heat_score +=1
        self.decay+=3
        if article_image:self.images.add(article_image) 
        self.last_updated_at = datetime.now(timezone.utc).isoformat()

    def update_title(self, title:str):
        self.title = title

    def update_summary(self, summary:str):
        self.summary = summary

    def update_report(self, report: str):
        self.report = report

    def update_story_text(self, story_text:str):
        self.story_text = story_text
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj
    
    def to_dict(self):
        def serialize(obj):
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(v) for v in obj]
            elif hasattr(obj, 'tolist'):  # for numpy arrays
                return obj.tolist()
            else:
                return obj

        return {
            "narrative_id": serialize(self.narrative_id),
            "title": serialize(self.title),
            "summary": serialize(self.summary),
            "created_at": serialize(self.created_at),
            "last_updated_at": serialize(self.last_updated_at),
            "source_article_ids": serialize(self.source_article_ids),
            "chunks": serialize(self.chunks),
            "heat_score": serialize(self.heat_score),
            "view_points": serialize(self.view_points),
            "images": list(serialize(self.images)),  # Convert set to list
            "sentiment_trend": serialize(self.sentiment_trend),
            "topic": serialize(self.topic),
            "decay": serialize(self.decay),
            "report": self.report,
            "sources": self.sources
        }