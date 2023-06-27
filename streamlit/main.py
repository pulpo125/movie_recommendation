import streamlit as st
import pandas as pd
import pymysql
from top_rating import create_idx, top_rating_df

# terminal open: streamlit run main.py

# mysql 연동
conn = pymysql.connect(host='127.0.0.1'
                , port=3306
                , user = 'root'
                , password='root1234'
                , db = 'movie_pj'
                , charset='utf8'
                ) 

cur = conn.cursor()

movies_sql = 'SELECT * FROM movies'
movies = pd.read_sql(movies_sql, conn)

# data load
movielens = pd.read_csv('../data/movielens.csv')

# streamlit 화면 시작
st.title('Title')

top_rating_idx = create_idx(movielens)
top_rating_df = top_rating_df(movies, top_rating_idx)
# st.experimental_data_editor(top_rating_df)
st.dataframe(top_rating_df)

conn.commit()
conn.close()


