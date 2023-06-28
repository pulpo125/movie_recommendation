import pickle as pkle
import streamlit as st
import pandas as pd
import pymysql
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity
from recommendation import compute_scores, user_recommendations

# mysql 연동
conn = pymysql.connect(host='127.0.0.1'
                , port=3306
                , user = 'root'
                , password='root1234'
                , db = 'movie_pj'
                , charset='utf8'
                ) 

# Data Load
movies_sql = 'SELECT * FROM movies'
movies = pd.read_sql(movies_sql, conn)
ratings_sql = 'SELECT * FROM ratings'
ratings = pd.read_sql(ratings_sql, conn)

# user_id
cursor = conn.cursor()
idx = cursor.fetchall(cursor.execute('select max(a.user_id) from users a'))
user_id = idx[0][0]
# user_id = 600

# similar
pvt=ratings.pivot_table(index='user_id',columns='movie_id',values='rating').fillna(0)
cos_sim=cosine_similarity(pvt,pvt)
cos_sim_df=pd.DataFrame(data=cos_sim)

similar_user_id = cos_sim_df[user_id].sort_values(ascending=False).index[1]

# CFModel
CFModel01 = tf.keras.models.load_model('../data/CFModel01.h5', compile=False)
CFModel01.embeddings = {
    'user_id': CFModel01.get_layer('user_embedding').weights[0].numpy(), # U (943, 30)
    'movie_id': CFModel01.get_layer('movie_embedding').weights[0].numpy() # V (1682, 30)
}

# recommendation
st.title('추천 결과입니다. :smile:')
similar_result = user_recommendations(CFModel01, movies, ratings, k=10, user_id=similar_user_id, exclude_rated=True)
st.write(f'유사한 유저 결과: {similar_user_id}')
st.dataframe(similar_result)

user_result = user_recommendations(CFModel01, movies, ratings, k=10, user_id=user_id, exclude_rated=True)
st.write(f'유저 결과: {user_id}')
st.dataframe(user_result)

conn.commit()
conn.close()