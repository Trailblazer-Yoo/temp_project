from mongoDB.DBUpdater import DBUpdater_ex
from pymongo import MongoClient
import pandas as pd

country_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam', 'Korea']

class DBconnect():
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db_ex = self.client['exchange']
        print('현재 존재하는 DB의 Collection 목록 : ', self.db_ex.list_collection_names().sort())
        
    def exchange_data(self):        
        df = []
        for country in country_name:
            coll = self.db_ex[country]
            mongo_df = pd.DataFrame(list(coll.find({}, {'_id' : 0})))
            df.append([country, mongo_df])
        # print(df[0]) # 오스트레일리아의 데이터 가져오기
        # df = [[country, pd.DataFrame(list(self.db_ex[country].find({}, {'_id' : 0})))] for country in country_name]
        print(df[0])
        
        return df

DB = DBconnect()
df = DB.exchange_data()

print(df[0][1]['buy'])