from typing import Dict, List
from models.article import Article


class ArticleStore:
    def __init__(self):
        self.store: Dict[str, Article] = {}

    def add(self, article:Article):
        
        self.store[article.article_id] = article
    
    def get(self, article_id:str):
        return self.store[article_id] if self.exists(article_id) else None
    
    def get_all(self) -> List[Article]:
        return list(self.store.values())
    
    def get_all_ids(self) -> List[str]:
        return list(self.store.keys())
    
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
            aid: {k: serialize(v) for k, v in vars(article).items()}
            for aid, article in self.store.items()
        }
    def save(self, path='article_store.json'):
        import json
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def load(self, path='article_store.json'):
        import json
        import os
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
            for aid, article_data in data.items():
                self.store[aid] = Article.from_dict(article_data)


    def exists(self, article_id:str):
        return article_id in self.store
    
    def remove(self, article_id):
        self.store.pop(article_id)