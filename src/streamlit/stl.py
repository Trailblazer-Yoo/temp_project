import streamlit as st
from datetime import datetime
import folium
import pandas as pd
import numpy as np
import execute
from streamlit_folium import folium_static
from dateutil.relativedelta import relativedelta

@st.experimental_singleton
def call_data():
    a = execute.region()
    
    return a

@st.experimental_singleton
def map():
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

    # add marker for Liberty Bell
    tooltip = "Liberty Bell"
    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    return m

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

region = call_data

st.title('🔥 일상에 찌든 당신 떠나조 🔥')
st.markdown('#### 여행에 필요한 정보(환율, 항공권 가격, 물가)를 제공하는 서비스입니다.')

folium_static(map())


with st.sidebar:
    ctrl_z = []
    dir = 0
    st.header('정보 입력')
    region = st.selectbox(
                '여행지를 선택해주세요',
                execute.region_dict.keys())

    start_date = st.date_input(
        '출발 날짜를 선택해주세요',
        datetime.now(), min_value = datetime.now()-relativedelta(years=1), max_value = datetime.now()+relativedelta(years=1))
    start_range, end_range = st.select_slider(
     "원하는 기간을 설정해주세요",
     options = ['0개월', '1개월', '2개월', '3개월', '4개월', '5개월', '6개월', '7개월', '8개월', '9개월', '10개월', '11개월', '12개월'],
    value = ('0개월', '1개월'))
    st.markdown(f'###### {start_range}부터 {end_range}까지 예측치 적용')
    st.markdown('#### 메인에 표시할 카테고리를 선택해주세요')
    ticket_button = st.checkbox('항공권')
    exchange_button = st.checkbox('환율')
    inflation_button = st.checkbox('물가')
    weather_button = st.checkbox('날씨')
    
if ticket_button:
    with st.container():
        st.write('항공권')
        chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
        st.line_chart(chart_data)
        
if exchange_button:
    with st.container():
        st.write('환율')
        st.line_chart(np.random.randn(50,1))
        date = datetime.now().month
        st.markdown(f'가장 저렴하게 살 수 있는 기간은 {date}월 입니다.')
        
if inflation_button:
    with st.container():
        st.write('물가')
        folium_static(map())
if weather_button:
    with st.container():
        st.write('Hello World')

    
    

    


    

    
    





    
# if st.button('환율 페이지'):
#     chapter = '환율'

    #     end_date = st.date_input(
    #     end_date = st.date_input(
    #         '떠나고 싶은 기간을 설정해주세요!',
    #         datetime.now().strftime('%Y-%m-%d')
    #     )
    #     return start_date, end_date
    # date()
