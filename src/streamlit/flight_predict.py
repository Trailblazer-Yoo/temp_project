class flight_predict:
    def __init__(self, flight_date, flight_country):
        from datetime import datetime; now = datetime.now()
        
        country_dict = {'코토카국제공항': 'ACC', '오알탐보국제공항': 'JNB', '케이프타운국제공항': 'CPT', '스키폴 국제공항': 'AMS',
                        '트리부반 국제공항': 'KTM', '오클랜드 국제공항': 'AKL', '퀸스타운공항': 'ZQN', '크라이스트처치 국제공항': 'CHC',
                        '타오위안 국제공항': 'TPE', '가오슝 국제공항': 'KHH', '타이중 국제공항': 'RMQ', '프랑크푸르트 국제공항': 'FRA',
                        '뮌헨 국제공항': 'MUC', '뒤셀도르프 국제공항': 'DUS', '블라디보스톡국제공항': 'VVO', '마카오 국제공항': 'MFM',
                        '코타키나발루 국제공항': 'BKI', '쿠알라룸푸르 국제공항': 'KUL', '베니토 후아레스 국제공항': 'MEX', '칸쿤국제공항': 'CUN',
                        '모하메드V국제공항': 'CMN', '말레 국제공항': 'MLE', '칭기즈 칸 국제공항': 'ULN', '마이애미 국제공항': 'MIA',
                        '매캐런 국제공항': 'LAS', '로건 국제공항': 'BOS', '포틀랜드 국제공항': 'PDX', '오헤어 국제공항': 'ORD',
                        '타코마 국제공항': 'SEA', '호놀룰루국제공항': 'HNL', '로스앤젤레스 국제공항': 'LAX', '워싱턴덜레스국제공항': 'IAD',
                        '달라스포트워스국제공항': 'DFW', '하츠필드잭슨애틀랜다국제공항': 'ATL', '존F.케네디 국제공항': 'JFK', '올랜도 국제공항': 'MCO',
                        '앤토니오 B.원 팻 국제공항': 'GUM', '사이판 국제공항': 'SPN', '탄손누트 국제공항': 'SGN', '노이바이 국제공항': 'HAN',
                        '캠란공항': 'CXR', '다낭 국제공항': 'DAD', '자반템 공항': 'BRU', '리우데자네이로공항': 'GIG',
                        '상파울루 공항': 'GRU', '킹파트공항': 'DMM', '젯다공항': 'JED', '킹할리드국제공항': 'RUH',
                        '반다라나이케국제공항': 'CMB', '제네바 국제공항': 'GVA', '취리히 국제공항': 'ZRH', '바라하스 국제공항': 'MAD',
                        '엘 프라트 국제공항': 'BCN', '창이 국제공항': 'SIN', '두바이 국제공항': 'DXB', '알막툼 국제공항': 'DWC',
                        '아부다비 국제공항': 'AUH', '미니스트로피스타리니국제공항': 'EZE', '이과수공항': 'IGR', '더블린 국제공항': 'DUB',
                        '우아리부메디엔공항': 'ALG', '키토국제공항': 'UIO', '히드로 국제공항': 'LHR', '런던시티 공항': 'LCY',
                        '퀸알리아국제공항': 'AMM', '타쉬켄트국제공항': 'TAS', '이맘호메이니공항': 'IKA', '벤구리온국제공항': 'TLV',
                        '카이로국제공항': 'CAI', '레오나르도다빈치 국제공항': 'FCO', '리나테 국제공항': 'LIN', '말펜사 국제공항': 'MXP',
                        '마르코폴로 국제공항': 'VCE', '인디라 간디 국제공항': 'DEL', '차트라파티 시바지 국제공항': 'BOM', '첸나이 국제공항': 'MAA',
                        '방갈로르공항': 'BLR', '네타지수바스찬드라보스국제공항': 'CCU', '도쿄 국제공항': 'HND', '나리타 국제공항': 'NRT',
                        '간사이 국제공항': 'KIX', '치토세공항': 'CTS', '나하공항': 'OKA', '후쿠오카공항': 'FUK',
                        '센트리아 나고야 국제공항': 'NGO', '베이징캐피탈국제공항': 'PEK', '심천공항': 'SZX', '대련국제공항': 'DLC',
                        '홍차오 국제공항': 'SHA', '장베이 국제공항': 'CKG', '바이윈 국제공항': 'CAN', '빈하이 국제공항': 'TSN',
                        '루커우 국제공항': 'NKG', '류팅 국제공항': 'TAO', '항주공항': 'HGH', '연길공항': 'YNJ',
                        '타오셴 국제공항': 'SHE', '바츨라프 하벨 국제공항': 'PRG', '산티아고국제공항': 'SCL', '도하국제공항': 'DOH',
                        '토론토국제공항': 'YYZ', '피에르 엘리오트 트뤼드 국제공항': 'YUL', '조모케냐타국제공항': 'NBO', '엘도라도국제공항': 'BOG',
                        '쿠웨이트국제공항': 'KWI', '자그레브공항': 'ZAG', '줄리어스니에레레국제공항': 'DAR', '수완나품 국제공항': 'BKK',
                        '푸켓 국제공항': 'HKT', '치앙마이 국제공항': 'CNX', '이스탄불 공항': 'IST', '아리아이공항': 'ROR',
                        '호르헤차베스국제공항': 'LIM', '포르텔라 국제공항': 'LIS', '쇼팽 국제공항': 'WAW', '샤를드골 국제공항': 'CDG',
                        '오를리 공항': 'ORY', '나디 국제공항': 'NAN', '헬싱키반타 국제공항': 'HEL', '클라크필드공항': 'CRK',
                        '막탄 세부 국제공항': 'CEB', '니노이아키노 국제공항': 'MNL', '프란츠리스트 국제공항': 'BUD', '시드니 국제공항': 'SYD',
                        '캔버라 국제공항': 'CBR', '멜버른 국제공항': 'MEL', '케언즈공항': 'CNS', '퍼스공항': 'PER',
                        '브리즈번공항': 'BNE', '홍콩 국제공항': 'HKG', '오슬로공항': 'OSL', '베르겐플레스랜드공항': 'BGO',
                        '트론하임공항': 'TRD', '솔라공항': 'SVG', '크리스티안산공항': 'KRS', '바레인국제공항': 'BAH',
                        '수카르노하타국제공항': 'CGK', '응우라이국제공항': 'DPS', '주안다국제공항': 'SUB', '롬복국제공항': 'LOP',
                        '요그야카르타공항': 'YIA', '쿠알라나무국제공항': 'KNO', '아마드야니공항': 'SRG', '후세인사스트라네가라공항': 'BDO',
                        '세핑안공항': 'BPN', '플로니아공항': 'MES'}

        self.now_date = now.date()
        self.flight_date = flight_date
        self.flight_code = country_dict[flight_country]

    def take_data(self):
        import pandas as pd
        from amadeus import Client, ResponseError

        flight_date = self.flight_date
        flight_code = self.flight_code
        now_date = self.now_date

        ama_data = pd.DataFrame(columns = ['여행지', '수집 날짜', '출발일', '마지막 티켓팅 가능 날짜',
                                        '수집 요일', '비행 요일', '비행_월', '비행 dday', '마지막 티켓팅 dday',
                                        '남은 좌석 수', '비행 시간', '출발 시간', '도착 시간',
                                        '경유 횟수', '항공기 코드 번호', '통화', '가격'])
        amadeus_data = pd.DataFrame(columns = ['여행지', '수집 날짜', '마지막 티켓팅 가능 날짜', '출발일', '비행_월', '수집 요일', '비행 요일', '비행 dday', '마지막 티켓팅 dday', '남은 좌석 수', '비행 시간', '출발 시간', '도착 시간', '경유 횟수', '항공기 코드 번호', '통화', '가격'])

        amadeus = Client(
            client_id = 'wPR1TcH4Jb3mdbL41ddUzZRrI8GUYm2F',
            client_secret = 'VGEmKb7Qn6pgxKjj'
        )

        try:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode = 'ICN',
                destinationLocationCode = flight_code,
                departureDate = flight_date,
                adults=1)
            
            for i in range(0, len(response.data)):
                day_data = response.data[i]
                now_date = pd.to_datetime(now_date)
                day = str(day_data['lastTicketingDate'])
                ticket_dday = pd.to_datetime(day) - now_date
                stop = len(day_data['itineraries'][0]['segments']) -1
                hour = day_data['itineraries'][0]['duration'].lstrip('PT').rstrip('M').split('H')
                dep = pd.to_datetime(day_data['itineraries'][0]['segments'][0]['departure']['at'])
                arr = pd.to_datetime(day_data['itineraries'][0]['segments'][stop]['arrival']['at'])
                flight_dday = dep - now_date
                
                if hour[1] == '': hour[1] = 0
                
                amadeus_data.loc[i] = [flight_code,
                                    ''.join([str(now_date)[0:4], '-', str(now_date)[5:7], '-', str(now_date)[8:10]]),
                                    ''.join([day[0:4], '-', day[5:7], '-', day[8:10]]),
                                    ''.join([str(dep.year), '-', str(dep.month), '-', str(dep.day)]),
                                    dep.month,
                                    now_date.dayofweek,
                                    dep.dayofweek,
                                    flight_dday.days,
                                    ticket_dday.days,
                                    day_data['numberOfBookableSeats'],
                                    round(int(hour[0]) + int(hour[1])/60, 1),
                                    round(int(dep.hour) + int(dep.minute)/60, 1),
                                    round(int(arr.hour) + int(arr.minute)/60, 1),
                                    stop,
                                    day_data['itineraries'][0]['segments'][0]['aircraft']['code'],
                                    day_data['price']['currency'],
                                    float(day_data['price']['total'])]

            ama_data = ama_data.append(amadeus_data, ignore_index = True)

        except ResponseError as error:
            print(day, filght_code, error)
            
        self.ama_data = ama_data

    def predict_data(self):
        import joblib
        import numpy as np
        import pandas as pd

        ama_data = self.ama_data

        model = joblib.load('flight_price.obj')
        
        model_date = pd.DataFrame(columns = ['여행지', '수집 요일', '비행 요일', '비행_월', '비행 dday', '마지막 티켓팅 dday',
                                        '남은 좌석 수', '비행 시간', '출발 시간', '도착 시간',
                                        '경유 횟수', '항공기 코드 번호'])
        
        price = np.log1p(ama_data['가격'])

        ds_x = ama_data.drop(['출발일', '수집 날짜', '마지막 티켓팅 가능 날짜', '통화', '가격'], axis = 1)

        for i in range(0, len(ds_x)):
            price_date = price[i]
            for j in range(0, int(ds_x.iloc[i]['마지막 티켓팅 dday']) + 1):
                date = ds_x.iloc[i]
                date['수집 요일'] = (int(date['수집 요일']) + j) % 7
                date['비행 dday'] = int(date['비행 dday']) - j
                date['마지막 티켓팅 dday'] = int(date['마지막 티켓팅 dday']) - j
                date['현재 가격'] = price_date
                
                model_date = model_date.append(date, ignore_index = True)
        predict_price = model_date.drop('현재 가격', axis = 1)

        cat_features = ['여행지', '항공기 코드 번호']
        int_features = ['수집 요일', '비행 요일', '비행_월', '비행 dday', '마지막 티켓팅 dday', '남은 좌석 수', '경유 횟수']

        for i in enumerate(cat_features):
            ca = i[1]
            predict_price[ca] = predict_price[ca].astype('category')
        
        for j in enumerate(int_features):
            ints = j[1]
            predict_price[ints] = predict_price[ints].astype('int')

        log_price = model.predict(predict_price)
        model_date['예측 가격'] = np.exp(log_price)
        
        predict_flight = pd.DataFrame(columns = ['dday', 'predict_price'])
        for l in range(model_date['비행 dday'][0], -1, -1):
            pre_price = model_date['예측 가격'][model_date['비행 dday'] == l].mean()
            one_data = {'dday' : l, 'predict_price' : pre_price}
            predict_flight = predict_flight.append(one_data, ignore_index = True)

        self.predict_flight = predict_flight

    def view_price(self):
        
        import plotly.express as px
        import streamlit as st

        predict_flight = self.predict_flight

        fig = px.line(predict_flight, x = 'dday', y = 'predict_price', title = '단위: EUR', template='plotly_white')
        fig['layout']['xaxis']['autorange'] = 'reversed'
        st.plotly_chart(fig)