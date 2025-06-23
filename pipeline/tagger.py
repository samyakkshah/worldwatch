from models.chunk import Chunk

def tagger(chunk:dict, article_id:str):
    return Chunk(chunk, article_id)