import pandas as pd
import config
from typing import Dict
import requests
articles = pd.read_csv(config.ALOE_ARTICLES)

for article in articles.iterrows():
    request_data: Dict[str, str] = dict()
    article_content: Dict[str, str] = dict(article[1])
    print(article_content)
    response = requests.post("http://localhost:8002/knowledge_extraction_to_neo4j?neo4j_url=asdf", json=article_content)
    print(response.content)

article: tuple
