from typing import Dict, List, Optional
from models.chunk import Chunk
from models.narrative import Narrative

class NarrativeStore:

    def __init__(self):
        self.store: Dict[str, Narrative] = {}
    
    def add(self, narrative: Narrative):
        self.store[narrative.narrative_id] = narrative
    
    def get(self, narrative_id: str):
        return self.store[narrative_id] if self.exists(narrative_id) else None

    def update(self, narrative_id: str, chunks: List[Chunk], article_source:str, article_id:str, article_image:Optional[str] = None):
        return self.store[narrative_id].update(chunks, article_source, article_id, article_image)
    
    def get_all(self) -> List[Narrative]:
        return list(self.store.values())

    def update_title(self, narrative_id:str, title: str):
        self.store[narrative_id].update_title(title)

    def update_summary(self, narrative_id:str, summary: str):
        self.store[narrative_id].update_summary(summary)

    def update_story_text(self, narrative_id:str, story_text: str):
        self.store[narrative_id].update_story_text(story_text)
        
    def exists(self, narrative_id):
        return narrative_id in self.store
    
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

        return [
            {k: serialize(v) for k, v in vars(narrative).items()}
            for _, narrative in self.store.items()
        ]

    def save(self, path='narrative_store.json'):
        import json
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def load(self, path='narrative_store.json'):
        import json
        import os
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
            for narrative_data in data:
                self.store[narrative_data["narrative_id"]] = Narrative.from_dict(narrative_data)

    def get_top_by_heat(self, k:int):
        import heapq
        top_heat_narratives = []
        for narrative in self.store.values():
            heapq.heappush(top_heat_narratives , (narrative.heat_score, narrative))
        
        return heapq.nlargest(k, top_heat_narratives , key=lambda x: x[0])

    def filter_by_topic(self, topic:str):
        pass

    def remove_or_merge(self, narrative_id):
        pass