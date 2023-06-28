import streamlit as st
import pandas as pd
import pymysql
from top_rating import get_top_idx, get_top_movies

# terminal open: cd streamlit -> streamlit run user_rating.py

## mysql 연동
conn = pymysql.connect(host='127.0.0.1'
                , port=3306
                , user = 'root'
                , password='root1234'
                , db = 'movie_pj'
                , charset='utf8'
                ) 

cur = conn.cursor()

## data load
# movies table
# movies_sql = 'SELECT * FROM movies'
# movies = pd.read_sql(movies_sql, conn)

# movielens table
movielens = pd.read_csv('../data/movielens.csv')

## streamlit
# header
st.title('환영합니다!')
st.subheader('좋아하는 :red[영화]를 선택한 후 :red[평점]을 남겨주세요. :smile:')

# contents
# info
st.write('**1(나쁨)~5(좋음) 사이로 평점을 입력해주세요.**')
st.write("**평가할 영화가 없다면 :red['Next']버튼을 눌러 주세요. 새로운 영화가 나타납니다.**")
st.write("**총 10개 이상의 영화를 평가해야 좋은 추천을 받을 수 있습니다.**")

# 좋아하는 영화 선택
top_movie_id = get_top_idx(movielens)
top_rating_movies = get_top_movies(movielens, top_movie_id)
cnt=0
def get_movie_list():
    movie_top10=[]
    for i in range(10):
        if top_rating_movies:
            movie_top10.append(top_rating_movies.pop(0))
    return movie_top10
#처음 영화 리스트를 가져옴
movie_top10=get_movie_list()
# 좋아하는 영화 선택
favorite_movies = st.multiselect('좋아하는 영화를 선택해주세요.', movie_top10[cnt:cnt+10])

if st.button('Next'):
   cnt+=10
   movie_top10=get_movie_list()
   favorite_movies = st.multiselect('좋아하는 영화를 선택해주세요.', movie_top10[cnt:cnt+10])
top_rating_movies    
rating_list = []
for i in range(len(top_rating_movies)):
    rating = st.slider(f'{top_rating_movies[i]}의 평점을 입력해주세요.', 0, 5)
    rating_list.append(rating)

rating_cnt = len(rating_list) - rating_list.count(0)

if rating_cnt == 0:
    st.button('제출', disabled=True)
else:
    btn_state = st.button('제출', disabled=False)

## db insert
if btn_state:
    # user_rating 
    user_rating_dic = list(zip(top_movie_id, rating_list))
    
    # db ratings 테이블에 insert
    for i in range(len(user_rating_dic)):
        cur.execute(f"INSERT INTO ratings (user_id, movie_id, rating) VALUES \
                ((select max(a.user_id)+1 from users a), {user_rating_dic[i][0]}, {user_rating_dic[i][1]});") 
    st.write('제출이 완료되었습니다.')

# else:
#     st.write('없음')



conn.commit()
conn.close()