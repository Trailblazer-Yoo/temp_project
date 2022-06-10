import streamlit as st
from datetime import datetime
import folium
import pandas as pd
import numpy as np
import execute
from streamlit_folium import folium_static
from dateutil.relativedelta import relativedelta
import streamlit.components.v1 as components # html파일 보여주기위해
import joblib
import flight_predict as fp
import plotly.express as px

from PIL import Image


dic_coun_code = joblib.load('dic_coun_code.obj') # 국가 / 공항코드 딕셔너리
dic_code_geo = joblib.load('dic_code_geo.obj') # 공항코드 / 위경도 딕셔너리
dic_code_air = joblib.load('dic_code_air.obj') # 공항코드 / 공항명 딕셔너리
dic_fin_geocode = joblib.load('dic_fin_geocode.obj') # 국가별 위경도 딕셔너리
dic_coun_air = joblib.load('dic_coun_air.obj') # 나라 / 공항명 딕셔너리

@st.experimental_singleton
def call_data():
    a = execute.region()
    
    return a

@st.experimental_singleton
def call_exchange():
    a = execute.preprocess()
    b = execute.lstm()
    return a, b

pre, lstm = call_exchange()

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

region = call_data

st.title('🔥 일상에 찌든 당신 떠나조 🔥')
st.markdown('#### 여행에 필요한 정보(환율, 항공권 가격, 물가)를 제공하는 서비스입니다.')

with st.sidebar:
    ctrl_z = []
    dir = 0
    st.header('정보 입력')
    region = st.selectbox(
                '여행지를 선택해주세요',
                execute.region_dict.keys())
   
    with st.sidebar.expander(region):
        option1 = st.selectbox('공항을 선택해주세요',dic_coun_air[region])

    start_date = st.date_input(
        '출발 날짜를 선택해주세요',
        datetime.now(), min_value = datetime.now()-relativedelta(years=1), max_value = datetime.now()+relativedelta(years=1))
    arr_date = st.date_input(
        '도착 날짜를 선택해주세요',
        datetime.now(), min_value = datetime.now()-relativedelta(years=1), max_value = datetime.now()+relativedelta(years=1))
   
    st.markdown('#### 메인에 표시할 카테고리를 선택해주세요')
    ticket_button = st.checkbox('항공권')
    exchange_button = st.checkbox('환율')
    inflation_button = st.checkbox('물가')
    weather_button = st.checkbox('날씨')
    wordcloud_button = st.checkbox('워드클라우드')
    
if ticket_button:
    with st.container():
        st.header("항공권")
        st.write('국가별 공항 위치와 선택한 공항까지의 항공권 가격 동향을 알려드립니다.')
        airmap = folium.Map(location=dic_fin_geocode[region], zoom_start=4)

        for i in range(0, len(dic_coun_code[region])):
            folium.Marker(dic_code_geo[dic_coun_code[region][i]],
                    tooltip=str(*dic_code_air[dic_coun_code[region][i]]),
                    popup=dic_coun_code[region][i],
                    icon=folium.Icon(
                                        color="lightblue",
                                        icon_color="white",
                                        icon="glyphicon glyphicon-plane",
                                        angle=50,
                                        prefix="glyphicon")
                ).add_to(airmap)

        folium_static(airmap)

        pred = fp.flight_predict(arr_date, option1)
        pred.take_data()
        pred.predict_data()
        
        pred.view_price()

        
if exchange_button:
    with st.container():
        df, date, ex = pre.daily_preprocessing('Canada')
        st.write('원화 대비 외국 화폐 환율')
        st.line_chart(ex[len(ex) - 100:])
        exchange = lstm.model_run(df)[0]
        st.write("내일의 예측 환율은 :", str(exchange), 'CAD 입니다.')

        
# 물가 지도 추가
if inflation_button: 
    with st.container():
        st.header("물가 정보")
        st.write('*마우스를 활용하여 확대 축소 및 전체화면을 사용해보세요!')
        HtmlFile = open("world_inflation_info.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        print(source_code)
        components.html(source_code, width = 850 , height = 600)

# 날씨 html 추가
import os
path = "./weekly_weather"
file_list = os.listdir(path)

path2 = "./monthly_temp"
file_list2 = os.listdir(path2)

if weather_button:
    with st.container():
        st.header("날씨") 
        st.write('주간 일기예보와 월 평균 기온 정보를 제공합니다.')

        month_weather = st.selectbox('도시를 선택해주세요',execute.region_dict[region])
        if month_weather:
            st.write( month_weather, "의 월 평균 기온 정보입니다.")
            search2 = list(filter(lambda x: month_weather in x, file_list2))
            search2 = str(search2).replace("['","").replace("']","")
            HtmlFile = open("./monthly_temp/"+search2, 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            print(source_code)
            components.html(source_code, width = 800 , height = 600)
        
        st.write(" (실시간) 국가별 주간 일기 예보 ")
        kotra_weather = st.selectbox ("국가리스트",['선택하세요','대만', '라오스', '말레이시아', '몽골', '미얀마', '방글라데시', '베트남', '스리랑카',
        '싱가포르', '아제르바이잔', '우즈베키스탄', '인도', '인도네시아', '일본', '중국', '카자흐스탄', '캄보디아', '태국', '파키스탄', '필리핀',
        '홍콩', '미국', '캐나다', '과테말라', '도미니카공화국', '멕시코', '브라질', '아르헨티나', '에콰도르', '칠레', '콜롬비아', '쿠바',
        '파나마', '파라과이', '페루', '그리스', '네덜란드', '덴마크', '독일', '러시아연방', '루마니아', '벨기에', '벨라루스', '불가리아', '세르비아',
        '스웨덴', '스위스', '스페인', '슬로바키아', '영국', '오스트리아', '우크라이나', '이탈리아', '체코', '크로아티아', '터키', '폴란드', '프랑스', '핀란드',
        '헝가리', '모로코', '사우디아라비아', '수단', '아랍에미리트', '알제리', '오만', '요르단', '이라크', '이란', '이스라엘', '이집트', '카타르',
        '쿠웨이트', '가나', '나이지리아', '남아프리카공화국', '모잠비크', '에티오피아', '케냐', '코트디부아르', '탄자니아', '뉴질랜드', '호주'])
        
        if kotra_weather == '선택하세요':
            st.markdown("### 총 83개국의 주간 날씨를 제공하고 있습니다.")
        elif kotra_weather:
            st.write( kotra_weather, "의 주간 일기예보입니다.")
            search1 = list(filter(lambda x: kotra_weather in x, file_list))
            search1 = str(search1).replace("['","").replace("']","")
            HtmlFile = open("./weekly_weather/"+search1, 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            print(source_code)
            components.html(source_code, width = 800 , height = 600)

if wordcloud_button:
    with st.container():
        try:
            image = Image.open(f'wordcloud/{region}.png')
            st.write('선택 나라에 대한 주요 키워드입니다.')
            st.image(image)
        except: st.write('해당 국가의 워드클라우드를 준비 중입니다.')




