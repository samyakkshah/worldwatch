import hashlib

class Chunk:
    def __init__(self, chunk, article_id):
        encoded_text = chunk['body'].encode("utf-8")
        self.chunk_id = hashlib.sha256(encoded_text).hexdigest()
        self.article_id = article_id
        self.narrative_id = ''
        self.chunk_order = chunk['idx']
        self.text = chunk['body']
        self.embedding = chunk['embedding']
        self.sentiment = chunk['sentiment']
    
    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj