import streamlit as st
import pandas as pd
import pymysql
from top_rating import create_idx, top_rating_df
import os.path
import pickle as pkle
from streamlit_js_eval import streamlit_js_eval

# terminal open: streamlit run member.py
st.title('당신의 오늘 영화는 어떤 것입니까?')
# mysql 연동
conn = pymysql.connect(host='127.0.0.1'
                , port=3306
                , user = 'root'
                , password='root1234'
                , db = 'movie_pj'
                , charset='utf8'
                ) 

cursor = conn.cursor()
pages=['page1','page2','page3']
if os.path.isfile('next.p'):
    next_clicked = pkle.load(open('next.p', 'rb'))
    print('next_clicked:', next_clicked)
#     if next_clicked == len(pages):
#         next_clicked = 0 
# else:
#     next_clicked = 0 

# if 0:
#     next_clicked = next_clicked+1
# if next_clicked == len(pages):
#         next_clicked = 0 

choice = st.sidebar.radio("Pages",('page1','page2', 'page3'), index=next_clicked)
pkle.dump(pages.index(choice), open('next.p', 'wb'))

if choice=='page1':
    st.subheader('당신의 영화를 추천해드립니다 정보를 입력하세요!')
    name=st.text_input("당신의 이름을 입력하세요")
    age=st.text_input("당신의 나이를 입력하세요(만나이기준)")
    st.write("당신의 성별을 입력하세요")
    pick=['M','F']
    status=st.radio('성별',pick)
    if status==pick[0]: 
        sex=pick[0]
    elif status==pick[1]:
        sex=pick[1]
    oc=st.text_input("당신의 직업을 입력해주세요")

    button_state = st.button("제출")

    if button_state:
        sql=f'Insert into users(user_id,age,sex,occupation) values((select max(a.user_id)+1 from users a), {int(age)}, "{sex}", "{oc}");'
        cursor.execute(sql)
        conn.commit()
        conn.close()
        st.text('데이터가 반영이 되었습니다 다음 페이지로 넘어가 주세요')
        import time
        time.sleep(2)

        choice = 'page2'
        pkle.dump(pages.index(choice), open('next.p', 'wb'))
        print('버튼 한 번 클릭')
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
    
elif choice=='page2':
    st.title('page 2')
