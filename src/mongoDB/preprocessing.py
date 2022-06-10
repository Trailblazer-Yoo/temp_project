import numpy as np
import pandas as pd
import requests
from pymongo import MongoClient

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
        self.client = MongoClient('localhost', 27017)
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
        elif country == 'Israel' or country == 'New-zealand':
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
        elif country == 'Israel' or country == 'New-zealand':
            pass
        
        date_time = pd.to_datetime(df.pop('date'), format='%Y-%m')
        df = df.astype('float')
        
        return df
    
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
        
        return df