import pickle as pkle
import streamlit as st
import pandas as pd
import pymysql
import tensorflow as tf
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
# users_sql = 'SELECT * FROM users'
# users = pd.read_sql(users_sql, conn)
ratings_sql = 'SELECT * FROM ratings'
ratings = pd.read_sql(ratings_sql, conn)

# user_id
# cursor = conn.cursor()
# user_id = cursor.execute('select max(a.user_id) from users a')
user_id = 600

# CFModel
CFModel01 = tf.keras.models.load_model('../data/CFModel01.h5', compile=False)
CFModel01.embeddings = {
    'user_id': CFModel01.get_layer('user_embedding').weights[0].numpy(), # U (943, 30)
    'movie_id': CFModel01.get_layer('movie_embedding').weights[0].numpy() # V (1682, 30)
}


result_df = user_recommendations(CFModel01, movies, ratings, k=10, user_id=user_id, exclude_rated=True)
st.dataframe(result_df)

conn.commit()
conn.close()