import pandas as pd
import numpy as np
from ast import literal_eval

org_data = pd.read_csv('./archive/movies_metadata.csv')
org_keywords = pd.read_csv('./archive/keywords.csv')


data = org_data[['id', 'genres', 'vote_average', 'vote_count',
                 'popularity', 'title', 'overview']]
keywords = org_keywords[['keywords']]

data['keywords'] = keywords.loc[['name']]

m = data['vote_count'].quantile(0.9)
data = data.loc[data['vote_count'] >= m]

C = data['vote_average'].mean()


def weighted_rating(x, m=m, C=C):
    v, R = x['vote_count'], x['vote_average']
    return (v / (v + m) * R) + (m / (v + m) * C)


data['score'] = data.apply(weighted_rating, axis=1)
data['genres'] = data['genres'].apply(literal_eval)
data['keywords'] = data['keywords'].apply(literal_eval)

data['genres'] = data['genres'].apply(
    lambda x: [d['name'] for d in x]).apply(lambda x: " ".join(x))
data['keywords'] = data['keywords'].apply(
    lambda x: [d['name'] for d in x]).apply(lambda x: " ".join(x))

data.head(2)
