from agents.crawler_agent import getNews
from store.chunk_store import ChunkStore
from store.narrative_store import NarrativeStore
from store.article_store import ArticleStore
from models.article import Article
from pipeline.graph import run_pipeline

def run_batch_pipeline():
    chunk_store = ChunkStore()
    chunk_store.load('data/chunk_store.json')

    narrative_store = NarrativeStore()
    narrative_store.load('data/narrative_store.json')

    article_store = ArticleStore()
    article_store.load('data/article_store.json')

    payload, status = getNews()
    if status == 200:
        articles = payload["articles"]    
        for new_article in articles[:100]:

            article = Article(new_article)
            article_store.add(article)
            
            
            print(f"Processing Article: {article.title}")
            try:
                final_state = run_pipeline(article, chunk_store, narrative_store)
                print(f"Processed: {final_state}")
            except Exception as e:
                title = article.get('title', 'Unknown') if isinstance(article, dict) else str(article)
                print(f"❌ Failed to process article: {title}")
                print("Error:", e)
    else:
        print(payload["message"])

    print(f"Narratives created: {len(narrative_store.get_all())}")
    article_store.save('data/article_store.json')
    chunk_store.save('data/chunk_store.json')
    narrative_store.save('data/narrative_store.json')


if __name__ == '__main__':
    run_batch_pipeline()