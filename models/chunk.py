import hashlib

class Chunk:
    """
        Initializes a Chunk instance with the provided chunk data and article ID.

        Parameters:
            chunk (dict): A dictionary containing the following keys:
                - 'body' (str): The text content of the chunk.
                - 'idx' (int): The order/index of the chunk within the article.
                - 'embedding' (Any): The embedding representation of the chunk.
                - 'sentiment' (Any): The sentiment analysis result for the chunk.
            article_id (str): The unique identifier of the article to which this chunk belongs.

        Attributes:
            chunk_id (str): A SHA-256 hash of the chunk's body, used as a unique identifier.
            article_id (str): The unique identifier of the article.
            narrative_id (str): The identifier for the narrative, initialized as an empty string.
            chunk_order (int): The order/index of the chunk within the article.
            text (str): The text content of the chunk.
            embedding (Any): The embedding representation of the chunk.
            sentiment (Any): The sentiment analysis result for the chunk.
        """
    def __init__(self, chunk, article_id):
        
        encoded_text = chunk['body'].encode("utf-8")
        self.chunk_id = hashlib.sha256(encoded_text).hexdigest()
        self.article_id = article_id
        self.narrative_id = ''
        self.chunk_order = chunk['idx']
        self.text = chunk['body']
        self.embedding = chunk['embedding']
        self.sentiment = chunk['sentiment']
        self.topics = chunk["topics"]
    
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
            'chunk_id': self.chunk_id,
            'article_id': self.article_id,
            'narrative_id': self.narrative_id,
            'chunk_order': self.chunk_order,
            'text': self.text,
            'embedding': serialize(self.embedding),
            'sentiment': serialize(self.sentiment)
        }