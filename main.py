import streamlit as st
import os
import base64
import pandas as pd
from datetime import datetime
import time
from app.date import *
from app.region import *
from app.genre import *
from app.performance import *
from app.facility import *
from app.visualization import *
from app.recommendation import *

st.set_page_config(page_title="Your App Title", page_icon="🌞", layout="centered", initial_sidebar_state="auto", theme="light")

st.markdown("""
    <style>
    body {
        background-color: #E8E8E8; 
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
            
    .mac-window {
        background-color: #F0F0F0; 
        border-radius: 12px; 
        padding: 30px; 
        margin: 20px auto;
        width: 100%; 
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
            
    .title {
        display: flex;
        align-items: center;
    }

    /* Mac Buttons */
    .mac-buttons {
        display: flex;
        gap: 8px;
        margin-right: 20px;
        margin-top: -20px;
    }
            
    .mac-button {
        width: 15px;
        height: 15px;
        border-radius: 50%;
        display: inline-block;
    }
    .mac-button-red {
        background-color: #FF605C;
    }
    .mac-button-orange {
        background-color: #FFBD44;
    }
    .mac-button-green {
        background-color: #00CA4E;
    }

    /* Title Styling */
    h1 {
        color: #333333; 
        font-size: 24px;
        line-height: 5px; 
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        margin-top: -30px;
    }

    /* Menu */
    .stButton > button {
        background-color: #F0F0F0
        color: #333333;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        cursor: pointer;
        font-size: 16px;
        margin: 10px auto;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        display: block;
    }       

    </style>
    """, unsafe_allow_html=True)

# Base64 이미지 인코딩 함수
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Base64 이미지 삽입 및 클릭 이벤트 설정
image_path = "imgs/logo.png"
if os.path.exists(image_path):
    base64_image = get_base64_image(image_path)
    st.markdown(f"""
        <style>
        img.clickable {{
            cursor: pointer;
            width: 300px;
        }}
        </style>
        <img class="clickable" src="data:image/png;base64,{base64_image}" onclick="menuRedirect()">
        <script>
        function menuRedirect() {{
            window.location.search = "?menu=true";
        }}
        </script>
    """, unsafe_allow_html=True)
else:
    st.error("Image not found!")

# 쿼리 파라미터 확인 및 세션 상태 변경
query_params = st.query_params
if "menu" in query_params:
    if st.session_state.context != "menu":
        st.session_state.context = "menu"
        st.experimental_rerun()



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = "menu" 

if "date" not in st.session_state:
    st.session_state.date = None

                        
if st.session_state.context == "menu":
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("원하는 메뉴를 선택하세요.")

        if st.button("기간별 예매 통계 조회"):
            st.session_state.context = "date"
            st.rerun()

        if st.button("지역별 예매 통계 조회"):
            st.session_state.context = "region"
            st.rerun()

        if st.button("장르별 예매 통계 조회"):
            st.session_state.context = "genre"
            st.rerun()

        if st.button("공연별 예매 통계 조회"):
            st.session_state.context = "performance"
            st.rerun()

        if st.button("공연 시설 상세 조회"):
            st.session_state.context = "facility"
            st.rerun()
        
        if st.button("공연 추천"):
            st.session_state.context = "recommendation"
            st.rerun()


if prompt := st.chat_input("질문을 입력하세요."):
    st.chat_message("user").markdown(prompt)
    
    if st.session_state.context == "date":
        if st.button("이전 메뉴"):
            st.session_state.context = "menu"
        st.session_state.date = prompt
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 날짜는 **{st.session_state.date}**입니다.")
        st.chat_message("assistant", avatar="imgs/icon.png").markdown("통계 정보를 불러오고 있습니다.")
        result = date_analysis(st.session_state.date)
        date_visual(result)


    if st.session_state.context == "region":
        if st.button("이전 메뉴"):
            st.session_state.context = "menu"
        st.session_state.region_date = prompt
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 지역은 **{st.session_state.region}**입니다.")
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 날짜는 **{st.session_state.region_date}**입니다.")
        stdate, eddate = st.session_state.region_date.split('~')
        result = region_analysis(st.session_state.region, stdate, eddate)
        region_visual(result)

    if st.session_state.context == "genre":
        if st.button("이전 메뉴"):
            st.session_state.context = "menu"
        st.session_state.genre_date = prompt
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 장르는 **{st.session_state.genre}**입니다.")
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 날짜는 **{st.session_state.genre_date}**입니다.")
        stdate, eddate = st.session_state.genre_date.split('~')
        result = genre_analysis(st.session_state.genre, stdate, eddate)
        genre_visual(result)

    if st.session_state.context == "performance":
        if st.button("이전 메뉴"):
            st.session_state.context = "menu"
        st.session_state.performance = prompt
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 공연은 **{st.session_state.performance}**입니다.")
        st.chat_message("assistant", avatar="imgs/icon.png").markdown("공연 정보를 불러오고 있습니다.")
        result = performance_analysis(st.session_state.performance)
        performance_visual(result)

    if st.session_state.context == "facility":
        if st.button("이전 메뉴"):
            st.session_state.context = "menu"
        st.session_state.facility = prompt
        st.chat_message("assistant", avatar="imgs/icon.png").markdown(f"입력하신 시설명은 **{st.session_state.facility}**입니다.")
        result = facility_analysis(st.session_state.facility)
        facility_visual(result)


elif st.session_state.context == "date":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("원하는 기간을 입력하세요.")
        st.markdown("<u>**입력 예시**</u>  \n 20240829  \n 202408  \n 2024", unsafe_allow_html=True)

elif st.session_state.context == "region":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("원하는 지역을 선택하세요.")  
        df = pd.read_excel('data/region_code_v2.xlsx')
        regions = df['region'].to_list()
        selected_region = st.selectbox("지역 선택", regions, placeholder="지역을 선택하세요.", key="selected_region", index=None)
        st.session_state.region = selected_region
       
    if selected_region:
        with st.chat_message("assistant", avatar="imgs/icon.png"):
            st.markdown(f"선택한 지역은: **{selected_region}**입니다.")
        with st.chat_message("assistant", avatar="imgs/icon.png"):
            st.markdown("시작 검색 기간과 종료 검색 기간을 입력하세요.")  
            st.markdown("<u>**입력 예시**</u>  \n 20240825~20240829", unsafe_allow_html=True)    

elif st.session_state.context == "genre":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("원하는 장르를 선택하세요.")  
        df = pd.read_excel('data/genre_code.xlsx')
        genre = df['genre'].to_list()
        code = df['code'].to_list()
        selected_genre = st.selectbox("장르 선택", genre, placeholder="장르를 선택하세요.", key="selected_genre", index=None)
        st.session_state.genre = selected_genre

    if selected_genre:
        with st.chat_message("assistant", avatar="imgs/icon.png"):
            st.markdown(f"선택한 장르는 **{selected_genre}**입니다.")
        with st.chat_message("assistant", avatar="imgs/icon.png"):
            st.markdown("시작 검색 기간과 종료 검색 기간을 입력하세요.")  
            st.markdown("<u>**입력 예시**</u>  \n 20240825~20240829", unsafe_allow_html=True)    

elif st.session_state.context == "performance":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("공연명을 입력하세요.")  

elif st.session_state.context == "facility":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("시설명을 입력하세요.")  
   
elif st.session_state.context == "recommendation":
    if st.button("이전 메뉴"):
        st.session_state.context = "menu"
    # 성별, 연령, 장르명, 공연지역명, 장당금액
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown("사용자의 성별, 선호 장르/지역/티켓 가격대를 선택하세요.")
        gender = ["남성", "여성"]
        selected_gender = st.selectbox("성별 선택", gender, placeholder="성별을 선택하세요.", key="selected_gender", index=None)

        current_year = 2024
        years = list(range(1900, current_year + 1))
        selected_year = st.selectbox("연령 선택", years, placeholder="나이대를 선택하세요.", key="selected_year", index=None)

        genre_code = pd.read_excel('data/genre_code.xlsx')
        genre = genre_code['genre'].to_list()
        code = genre_code['code'].to_list()
        selected_genre = st.selectbox("장르 선택", genre, placeholder="장르를 선택하세요.", key="selected_genre", index=None)

        region_code = pd.read_excel('data/region_code_v2.xlsx')
        regions = region_code['region'].to_list()
        selected_region = st.selectbox("지역 선택", regions, placeholder="지역을 선택하세요.", key="selected_region", index=None)

        price = ["10,000~20,000원", "20,000~30,000원", "30,000~40,000원", "30,000~40,000원", "40,000~50,000원", "50,000~100,000원", "100,000~200,000원"]
        selected_price = st.selectbox("가격대 선택", price, placeholder="가격대를 선택하세요.", key="selected_price", index=None)
        
        st.session_state.re_gender = selected_gender
        st.session_state.re_year = selected_year
        st.session_state.re_genre = selected_genre
        st.session_state.re_region = selected_region
        st.session_state.re_price = selected_price

        if selected_price:
            performance_names = recommend(selected_gender, selected_year, selected_genre, selected_region, selected_price)
            st.session_state.recommendation = '추천 공연은 '+', '.join(performance_names)+" 입니다."

    time.sleep(3)
    with st.chat_message("assistant", avatar="imgs/icon.png"):
         st.markdown("추천 공연을 불러오고 있습니다.")
    time.sleep(3)
    with st.chat_message("assistant", avatar="imgs/icon.png"):
        st.markdown(st.session_state.recommendation)
