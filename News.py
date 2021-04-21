from newsapi import NewsApiClient
import pandas as pd

API_KEY = "API KEY"
newsapi = NewsApiClient(api_key=API_KEY)
get_everything = newsapi.get_everything(q='bitcoin',
                                        sort_by='publishedAt',
                                        language='en')

articles = pd.DataFrame.from_dict(get_everything['articles'][:10])
articles['source'] = [source['name'] for source in articles['source']]
articles.to_csv("articles.csv", index=False)

