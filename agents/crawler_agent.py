import json
import dotenv
dotenv.load_dotenv()
import os
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ENV = os.getenv("ENV")

def getNews(directory="data"):
    data_path = os.path.join(directory, "test_data.json")
    if ENV == "dev":
        try:
            with open(data_path, "r") as json_file:
                articles = json.load(json_file)
                return {"message": "Loaded from local test_data", "articles": articles}, 200
        except Exception as e:
            return {"message": f"Error loading local data: {str(e)}"}, 500
        

    er = EventRegistry(apiKey = NEWS_API_KEY, allowUseOfArchive=False)
    categories = ["world", "business", "technology", "politics"]
    category_uris = [er.getCategoryUri(cat) for cat in categories]
    q = QueryArticlesIter(
    # here we don't use keywords so we will also get articles that mention immigration using various synonyms
        categoryUri= QueryItems.OR(category_uris),
        lang="eng"
    )

    try:
        articles = []
        for article in q.execQuery(er, sortBy="date", sortByAsc=False, maxItems=500):
            articles.append(article) 

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"{directory}/test_data.json", "w") as json_file:
            json.dump(articles, json_file, indent=4)

        return {"message": "Saved in test_data"}, 200

    except Exception as e:
        return {"message": f"Error {str(e)}"}, 500