import numpy as np
import pandas as pd
from pymongo import MongoClient
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.layers import Reshape, Dense, LSTM, GRU, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt

class region():
    def __init__(self):
        pass
        
region_dict = {'가나' : [''],
                '남아프리카공화국' : ['케이프타운','요하네스버스'],
                '네덜란드' : ['로테르담', '암스테르담', '헤이그'],
                '네팔': [''],
                '노르웨이' : ['오슬로','베르겐','스타방에르','트롬쇠','올레순'],
                '뉴질랜드' : ['남섬','오클랜드','웰링턴','타우랑가','해밀턴','파이히아'],
                '대만' : ['타이페이','타이중','가오슝','타이난','화롄','헝춘'],
                '독일' : ['베를린', '뮌헨', '함부르크', '프랑크푸르트', '쾰른', '슈투트가르트', 
                            '드레스덴', '뉘른베르크', '라이프치히', '하이델베르크', '브레멘', '뤼벡', 
                            '뷔르츠부르크', '아우크스부르크', '밤베르크', '로텐부르크 오프데어 타우버', 
                            '울름', '퓌센', '슈베린', '하멜른'],
                '러시아' : ['모스크바','상트페테르부르크','블라디보스토크','이르쿠츠크','노보시비르스크','하바롭스크'],
                '마카오' : [''],
                '말레이시아' : ['쿠알라룸푸르','페낭 섬','랑카위','말라카','코타키나발루','조호르바루','쿠칭'],
                '멕시코' : ['멕시코 시티','로스 카보스','플라야 델 카르멘','칸쿤','과달라하라',
                            '산미겔 데 아옌데','몬테레이','과나후아토'],
                '모로코' : [''],
                '몰디브' : [''],
                '몽골' : [''],
                '미국' : ['괌', '뉴욕','하와이','라스베이거스','샌프란시스코','로스앤젤레스'], 
                '바레인' : ['바레인'],
                '베트남' : ['호찌민','호이안','하노이','다낭','나트랑','후에','푸꾸옥','달랏','사파','닌빈','하롱'],
                '브라질' : ['리우데자네이루', '파라티', '포스두이구아수', '보니또'],
                '사우디아라비아' : ['리야드', '제다', '메카', '메디나', '얀부'],
                '스리랑카' : [''],
                '스위스' :  ['취리히','제네바','로잔','바젤','베른','루체른','루가노',
                        '체르마트','인터라켄','몽트뢰','그린델발트','라우터브루넨','벤겐'],
                '스페인' : ['그라나다', '네르하', '론다', '마드리드', '마요르카', '말라가', '바르셀로나', 
                            '발렌시아', '빌바오', '산타 쿠르스 데 테네리페', '산티아고 데 콤포스텔라', '세비야',
                             '시체스', '이비사', '코르도바', '톨레도'],
                '싱가포르' : ['싱가포르'],
                '아랍에미리트' : ['두바이','아부 다비'],
                '아르헨티나' : [''],
                '알제리' : [''],
                '에콰도르' : [''],
                '영국' : ['런던','에든버러','글래스고','버밍엄','맨체스터','리버풀','브리스틀','요크','브라이턴',
                        '뉴캐슬어폰타인','카디프','벨파스트','옥스퍼드','케임브리지','본머스'],
                '요르단' : ['암만','아카바','와디무사'],
                '우즈베키스탄' : [''],
                '이란' : [''],
                '이스라엘' : ['텔아비브','예루살렘'],
                '이집트' : [''],
                '이탈리아' : ['로마', '밀라노', '베네치아', '피렌체'],
                '인도' : ['뭄바이','뉴델리','고아','벵갈루루','자이푸르','콜카타','우다이푸르','바라나시','조드푸르'],
                '인도네시아' : ['발리','자바섬','자카르타','롬복','욕야카르타','빈탄섬'],
                '일본' : ['도쿄','오키나와','교토','오사카','삿포로','후쿠오카'],
                '중국' : ['상하이','베이징','광저우','선전','청두','하이난','시안','항저우','쑤저우','난징',
                        '톈진','칭다오','다롄','샤먼','충칭','하얼빈','쿤밍','구이린','리장',
                        '장자제','황산시', '옌타이','옌볜'],
                '체코' : ['프라하','카를로비 바리','체스키 크룸로프','올로모우츠'],
                '칠레' : [''],
                '카타르' : [''],
                '캐나다' : ['토론토','몬트리올','벤쿠버','오타와','캘거리','퀘벡','빅토리아',
                            '나이아가라 폭포 시티','휘슬러','밴프','옐로나이프'],
                '케냐' : [''],
                '콜롬비아' : [''],
                '쿠웨이트' : ['쿠웨이트'],
                '크로아티아' : [''],
                '탄자니아' : [''],
                '태국' : ['방콕','푸껫','치앙마이','코사무이','파타야','크라비','후아힌',
                        '카오락','코 창','치앙라이','피피섬','코사멧'],
                '터키' : ['이스탄불','앙카라','안탈리아','욀뤼데니즈','이즈미르','괴레메','파묵칼레'],
                '페루' : [''],
                '포르투갈' : ['리스본', '포르투'],
                '폴란드' : ['크라쿠프','바르샤바','그단스크','브로츠와프','포즈난','자코파네'],
                '프랑스' : ['파리', '브리타니', '보르도', '니스', '마르세유', '스트라스부르', 
                        '엑상프로방스', '칸', '아비뇽', '루앙', '콜마르', '아를', '몽생미셸', '생폴 드 방스'],
                '피지' : ['피지'],
                '핀란드' : ['로바니에미', '탐페레', '투르쿠', '헬싱키'],
                '필리핀' : ['세부','팔라완','마닐라','보라카이','보홀','바기오','다바오','따가이따이','바탕가스'],
                '헝가리' : ['부다페스트'],
                '호주' : ['시드니', '멜버른', '태즈메이니아', '브리즈번', '골드코스트', '애들레이드', '캔버라',     
                        '퍼스', '케언즈', '울런공', '앨리스 스프링스', '아폴로베이', '해밀턴 아일랜드', '율라라'],
                '홍콩' : ['홍콩']
                }


mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei',
              'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro',
                'Fiji', 'Hungary', 'India', 'Indonesia',
                'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia',
                'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia',
                'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand',
                'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei',
              'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro',
                'Fiji', 'Hungary', 'India', 'Indonesia',
                'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia',
                'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia',
                'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand',
                'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

class preprocess():
    def __init__(self):
        host = '35.78.27.97'
        port = '27017'
        self.client = MongoClient(f'mongodb://{host}:{port}')
        #self.client = MongoClient('localhost', 27017)
        self.db_ex = self.client['exchange']
        self.db_int = self.client['interest']
        self.db_inf = self.client['inflation']
        self.db_m1 = self.client['liquidity']
        
    def monthly_preprocessing(self, country):
        ex_ca = pd.DataFrame(list(self.db_ex[country].find({}, {'_id':0})))
        ex_ca['date'] = pd.to_datetime(ex_ca['date'])
        ex_ca = ex_ca.set_index('date')
        ex_ca['ex'] = np.log(ex_ca['buy'])
        ex_ca = ex_ca.resample(rule = 'M').last()
        
        df = ex_ca.reset_index()[['date','ex']]
        coll_int = self.db_int[country]
        inter = pd.DataFrame(list(coll_int.find({}, {'_id':0})))
        if '1' in inter.columns[1]:
            int_ko = pd.DataFrame(list(self.db_int['Korea1Y'].find({}, {'_id':0})))
            interest = pd.merge(inter, int_ko, on='date', how='inner')
            interest['int_spread'] = interest['interest1Y_y'] - interest['interest1Y_x'] 
            interest['date'] = pd.to_datetime(interest['date'])
            interest = interest[['date', 'int_spread']]

            df = pd.merge(df, interest, on='date', how = 'inner')
            df['date'] = df['date'].dt.strftime("%Y-%m")
        elif '2' in inter.colunns[1]:
            int_ko = pd.DataFrame(list(self.db_int['Korea2Y'].find({}, {'_id':0})))
            interest = pd.merge(inter, int_ko, on='date', how='inner')
            interest['int_spread'] = interest['interest1Y_y'] - interest['interest1Y_x'] 
            interest['date'] = pd.to_datetime(interest['date'])
            interest = interest[['date', 'int_spread']]

            df = pd.merge(df, interest, on='date', how = 'inner')
            df['date'] = df['date'].dt.strftime("%Y-%m")
        elif len(inter) == 0:
            pass

        inf = pd.DataFrame(list(self.db_inf[country + 'M'].find({}, {'_id':0})))
        infq = pd.DataFrame(list(self.db_inf[country + 'Q'].find({}, {'_id':0})))
        inflation_KOR = pd.DataFrame(list(self.db_inf['Korea' + 'M'].find({}, {'_id':0})))
        if len(inf) != 0:
            inf['inf_c'] = inf['inflation'].astype('float').pct_change()*100
            inflation_KOR['inf_kc'] = inflation_KOR['inflation'].astype('float').pct_change()*100
            inflation = pd.merge(inf, inflation_KOR[['date', 'inf_kc']], on='date', how='inner' )
            inflation['inf_spread'] = inflation['inf_kc'] - inflation['inf_c']
            df = pd.merge(df, inflation[['date', 'inf_spread']], on='date', how = 'inner')
        elif len(inf) == 0 and len(infq) != 0:
            infq['date'] = pd.to_datetime(infq['date']).dt.to_period('Q')
            infq = infq.set_index('date').astype('float')
            infq = infq.resample(rule = 'M').fillna(method= 'ffill')
            infq = infq.reset_index()
            infq['date'] = infq['date'].astype('str')
            infq['inf_c'] = infq['inflation'].astype('float').pct_change()*100
            inflation_KOR['inf_kc'] = inflation_KOR['inflation'].astype('float').pct_change()*100
            inflation = pd.merge(infq, inflation_KOR[['date', 'inf_kc']], on='date', how='inner' )
            inflation['inf_spread'] = inflation['inf_kc'] - inflation['inf_c']
            df = pd.merge(df, inflation[['date', 'inf_spread']], on='date', how = 'inner')
        elif len(inf) == 0 and len(infq) == 0:
            pass

        
        m1 = pd.DataFrame(list(self.db_m1[country + 'M'].find({}, {'_id':0})))
        m1q = pd.DataFrame(list(self.db_m1[country + 'Q'].find({}, {'_id':0})))
        if len(m1) != 0:
            m1_KOR = pd.DataFrame(list(self.db_m1['Korea' + 'M'].find({}, {'_id':0})))
            m1['m1'] = np.log(m1['liquidity'].astype('float'))
            m1_KOR['m1_k'] = np.log(m1_KOR['liquidity'].astype('float'))
            m1 = pd.merge(m1[['date','m1']], m1_KOR[['date', 'm1_k']], on='date', how='inner')
            m1['m1_spread'] = m1['m1_k'] - m1['m1']
            df = pd.merge(df, m1[['date', 'm1_spread']], on='date', how = 'inner')
        elif len(m1) == 0 and len(m1q) != 0:
            m1_KOR = pd.DataFrame(list(self.db_m1['Korea' + 'M'].find({}, {'_id':0})))
            m1q['date'] = pd.to_datetime(m1q['date']).dt.to_period('Q')
            m1q = m1q.set_index('date').astype('float')
            m1q = m1q.resample(rule = 'M').fillna(method= 'ffill')
            m1q = m1q.reset_index()
            m1q['date'] = m1q['date'].astype('str')
            m1q['m1'] = np.log(m1q['liquidity'].astype('float'))
            m1_KOR['m1_k'] = np.log(m1_KOR['liquidity'].astype('float'))
            m1q = pd.merge(m1q[['date','m1']], m1_KOR[['date', 'm1_k']], on='date', how='inner')
            m1q['m1_spread'] = m1q['m1_k'] - m1q['m1']
            df = pd.merge(df, m1q[['date', 'm1_spread']], on='date', how = 'inner')
        elif len(m1) == 0 and len(m1q) == 0:
            pass
        
        date_time = pd.to_datetime(df.pop('date'), format='%Y-%m')
        df = df.astype('float')
        graph = ex_ca[['date','buy']].set_index('date')
        
        return df, date_time, graph
    
    def daily_preprocessing(self, country):
        ex_ca = pd.DataFrame(list(self.db_ex[country].find({}, {'_id':0})))
        ex_ca['date'] = pd.to_datetime(ex_ca['date'])
        ex_ca['ex'] = np.log(ex_ca['buy'])
        df = ex_ca[['date','ex']]
        
        coll_int = self.db_int[country]
        inter = pd.DataFrame(list(coll_int.find({}, {'_id':0})))
        if '1' in inter.columns[1]:
            int_ko = pd.DataFrame(list(self.db_int['Korea1Y'].find({}, {'_id':0})))
        elif '2' in inter.colunns[1]:
            int_ko = pd.DataFrame(list(self.db_int['Korea2Y'].find({}, {'_id':0})))

        interest = pd.merge(inter, int_ko, on='date', how='inner')
        interest['int_spread'] = interest['interest1Y_y'] - interest['interest1Y_x'] 
        interest['date'] = pd.to_datetime(interest['date'])
        interest = interest[['date', 'int_spread']]

        df = pd.merge(df, interest, on='date', how = 'inner')
        
        inf = pd.DataFrame(list(self.db_inf[country + 'M'].find({}, {'_id':0})))
        infq = pd.DataFrame(list(self.db_inf[country + 'Q'].find({}, {'_id':0})))
        inflation_KOR = pd.DataFrame(list(self.db_inf['Korea' + 'M'].find({}, {'_id':0})))
        
        if len(inf) != 0:
            inf['inf_c'] = inf['inflation'].astype('float').pct_change()*100
            inflation_KOR['inf_kc'] = inflation_KOR['inflation'].astype('float').pct_change()*100
            inflation = pd.merge(inf, inflation_KOR[['date', 'inf_kc']], on='date', how='inner' )
            inflation['inf_spread'] = inflation['inf_kc'] - inflation['inf_c']
            inflation['date'] = pd.to_datetime(inflation['date']).dt.to_period('M')
            inflation = inflation.set_index('date')
            inflation = inflation.resample(rule = 'D').fillna(method= 'ffill')
            inflation = inflation.reset_index()
            inflation['date'] = pd.to_datetime(inflation['date'].astype('str'))
            df = pd.merge(df, inflation[['date', 'inf_spread']], on='date', how = 'inner')
        elif len(inf) == 0 and len(infq) != 0:
            infq['date'] = pd.to_datetime(infq['date']).dt.to_period('Q')
            infq = infq.set_index('date').astype('float')
            infq = infq.resample(rule = 'M').fillna(method= 'ffill')
            infq = infq.reset_index()
            infq['date'] = infq['date'].astype('str')
            infq['inf_c'] = infq['inflation'].astype('float').pct_change()*100
            inflation_KOR['inf_kc'] = inflation_KOR['inflation'].astype('float').pct_change()*100
            inflation = pd.merge(infq, inflation_KOR[['date', 'inf_kc']], on='date', how='inner' )
            inflation['inf_spread'] = inflation['inf_kc'] - inflation['inf_c']
            inflation['date'] = pd.to_datetime(inflation['date']).dt.to_period('M')
            inflation = inflation.set_index('date')
            inflation = inflation.resample(rule = 'D').fillna(method= 'ffill')
            inflation = inflation.reset_index()
            inflation['date'] = pd.to_datetime(inflation['date'].astype('str'))
            df = pd.merge(df, inflation[['date', 'inf_spread']], on='date', how = 'inner')
        elif len(inf) == 0 and len(infq) == 0:
            pass
        
        m1 = pd.DataFrame(list(self.db_m1[country + 'M'].find({}, {'_id':0})))
        m1q = pd.DataFrame(list(self.db_m1[country + 'Q'].find({}, {'_id':0})))
        if len(m1) != 0:
            m1_KOR = pd.DataFrame(list(self.db_m1['Korea' + 'M'].find({}, {'_id':0})))
            m1['m1'] = np.log(m1['liquidity'].astype('float'))
            m1_KOR['m1_k'] = np.log(m1_KOR['liquidity'].astype('float'))
            m1 = pd.merge(m1[['date','m1']], m1_KOR[['date', 'm1_k']], on='date', how='inner')
            m1['m1_spread'] = m1['m1_k'] - m1['m1']
            m1['date'] = pd.to_datetime(m1['date']).dt.to_period('M')
            m1 = m1.set_index('date')
            m1 = m1.resample(rule = 'D').fillna(method= 'ffill')
            m1 = m1.reset_index()
            m1['date'] = pd.to_datetime(m1['date'].astype('str'))
            df = pd.merge(df, m1[['date', 'm1_spread']], on='date', how = 'inner')
        elif len(m1) == 0 and len(m1q) != 0:
            m1_KOR = pd.DataFrame(list(self.db_m1['Korea' + 'M'].find({}, {'_id':0})))
            m1q['date'] = pd.to_datetime(m1q['date']).dt.to_period('Q')
            m1q = m1q.set_index('date').astype('float')
            m1q = m1q.resample(rule = 'M').fillna(method= 'ffill')
            m1q = m1q.reset_index()
            m1q['date'] = m1q['date'].astype('str')
            m1q['m1'] = np.log(m1q['liquidity'].astype('float'))
            m1_KOR['m1_k'] = np.log(m1_KOR['liquidity'].astype('float'))
            m1q = pd.merge(m1q[['date','m1']], m1_KOR[['date', 'm1_k']], on='date', how='inner')
            m1q['m1_spread'] = m1q['m1_k'] - m1q['m1']
            m1q['date'] = pd.to_datetime(m1q['date']).dt.to_period('M')
            m1q = m1q.set_index('date')
            m1q = m1q.resample(rule = 'D').fillna(method= 'ffill')
            m1q = m1q.reset_index()
            m1q['date'] = pd.to_datetime(m1q['date'].astype('str'))
            df = pd.merge(df, m1q[['date', 'm1_spread']], on='date', how = 'inner')
        elif len(m1) == 0 and len(m1q) == 0:
            pass
        
        date_time = pd.to_datetime(df.pop('date'), format='%Y-%m-%d')
        df = df.astype('float')
        graph = ex_ca[['date','buy']].set_index('date')
        
        return df, date_time, graph
    
class lstm():
    def __init__(self):
        pass
    
    def model_run(self, df):
        mean = df.mean()
        std = df.std()

        df = (df - mean) / std
        
        dfx = df# 반복횟수 600
        dfy = df['ex']

        window_size = 5
        data_size = 4

        x = dfx.values.tolist()
        y = dfy.values.tolist()

        data_x = []
        data_y = []
        for i in range(len(y) - window_size):
            _x = x[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
            _y = y[i + window_size]     # 다음 날 종가
            data_x.append(_x)
            data_y.append(_y)
        print(_x, "->", _y)

        train_size = int(len(data_y) * 0.9)
        train_x = np.array(data_x[0 : train_size])
        train_y = np.array(data_y[0 : train_size])

        test_size = len(data_y) - train_size
        test_x = np.array(data_x[train_size : len(data_x)])
        test_y = np.array(data_y[train_size : len(data_y)])

        # 모델 생성
        model = Sequential()
        model.add(LSTM(units=5, activation='tanh', return_sequences=True, input_shape=(window_size, data_size)))
        model.add(LSTM(units=5, activation='tanh'))
        model.add(Dense(units=1))
        model.summary()

        optimizer = optimizers.Adam(lr = 0.001)
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        # model.compile(optimizer=adam, loss='mean_squared_error')
        history = model.fit(train_x, train_y, epochs=10, batch_size=40, validation_split=0.1)
        pred_y = model.predict(test_x)

        return np.exp(pred_y[-1] * std['ex'] + mean['ex'])