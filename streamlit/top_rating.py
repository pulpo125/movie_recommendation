import pandas as pd

def get_top_idx(movielens):
    top_movie_id = list(movielens['movie_id'].value_counts().index)
    return top_movie_id[:50]

def get_top_movies(movielens, top_movie_id):    
    top_rating_movies = []
    for idx in top_movie_id:
        top_rating_movies.append(movielens.loc[movielens['movie_id'] == idx, 'title'].values[0])
    return top_rating_movies 