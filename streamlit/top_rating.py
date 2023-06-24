import pandas as pd

def create_idx(movielens, n=1):
    genre_cols = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 
                  'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    
    top_rating_idx = []
    for col in genre_cols:
        top_rating_idx += list(movielens.loc[movielens[col] == 1, 'movie_id'].value_counts()[:n].index)

    return set(top_rating_idx)

def top_rating_df(movies, top_rating_idx):    
    top_rating_df = pd.DataFrame()
    for idx in top_rating_idx:
        top_rating_df = pd.concat([top_rating_df, movies[movies['movie_id'] == idx]])
    
    top_rating_df.reset_index(drop=True, inplace=True)
    return top_rating_df