import pandas as pd 

def compute_scores(query_embedding, item_embeddings):
  """Computes the scores of the candidates given a query.
  Args:
    query_embedding: a vector of shape [k], representing the query embedding.
    item_embeddings: a matrix of shape [N, k], such that row i is the embedding
      of item i.
    measure: a string specifying the similarity measure to be used. Can be
      either DOT or COSINE.
  Returns:
    scores: a vector of shape [N], such that scores[i] is the score of item i.
  """
  u = query_embedding
  V = item_embeddings
  # if measure == COSINE:
  #   V = V / np.linalg.norm(V, axis=1, keepdims=True)
  #   u = u / np.linalg.norm(u)
  scores = u.dot(V.T)
  return scores

# @title User recommendations and nearest neighbors (run this cell)
def user_recommendations(model, movies, ratings, exclude_rated=False, k=6, user_id=570):
  USER_RATINGS = True
  if USER_RATINGS:
    scores = compute_scores(
        model.embeddings["user_id"][user_id], model.embeddings["movie_id"])
    score_key = 'dot' + ' score'
    df = pd.DataFrame({
        score_key: list(scores),
        'movie_id': movies['movie_id'],
        'titles': movies['title'],
        'genres': movies['all_genres'],
    })
    if exclude_rated:
      # remove movies that are already rated
      rated_movies = ratings[ratings.user_id == str(user_id)]["movie_id"].values
      df = df[df.movie_id.apply(lambda movie_id: movie_id not in rated_movies)]
    return (df.sort_values([score_key], ascending=False).head(k))