import hashlib

class Article:
    def __init__(self, article):
        self.article_id = hashlib.sha256(article["url"].encode("utf-8")).hexdigest()
        self.title = article["title"]
        self.url = article["url"]
        self.timestamp = article["dateTime"] or article['dateTimePub']
        self.source = article['source']['title']
        self.image_url = article['image']
        self.body = article['body']
        self.sentiment = article["sentiment"]

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj