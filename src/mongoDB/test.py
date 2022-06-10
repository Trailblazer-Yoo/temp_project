from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
host = '35.78.27.97'
port = '27017'
client_aws = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.

mongo_name = ['Australia', 'Bahrain', 'Brazil', 'Brunei', 'Cambodia','Canada', 'Hong Kong',
                'China', 'Czech', 'Denmark', 'Euro', 'Fiji', 'Hungary', 'India', 'Indonesia', 'Israel',
                'Japan', 'Jordan', 'Kuwait', 'Malaysia', 'Mexico', 'New Zealand',
                'Norway', 'Philippines', 'Poland', 'Russia', 'Saudi Arabia', 'Singapore', 'South Africa',
                'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'UAE', 'UK', 'USA', 'Vietnam']

db = client['inflation']
for country in ['Australia', 'Czech', 'Malaysia','New Zealand' ,'Switzerland']:
    coll = db[country + 'M']
    if len(list(coll.find({}))) > 0:
        data = list(coll.find({}, {'_id':0}))
        coll2 = db[country + 'Q']
        coll2.insert_many(data)

# db = client['exchange']
# db_in = client['interest']
# start_date = pd.to_datetime(db['USA'].find({})[0]['date']) ## 시작 날짜
# end_date = pd.to_datetime(list(db['USA'].find({}))[-1]['date']) ## 마지막 날짜
 
# dates = pd.date_range(start_date,end_date,freq='D')
# padding = pd.DataFrame({'date' : dates})
# padding['date'] = padding['date'].dt.strftime('%Y-%m-%d').astype('str')
# data = padding.to_dict('record')
# print(data)
# for d in ['exchange', 'interest']:
#     db = client[d]
#     for country in db.list_collection_names():
#         coll = db[country]
#         coll2 = client_aws[d][country]
#         data = list(coll.find({}, {'_id' : 0}))
#         coll2.insert_many(data)

# a = pd.read_csv('/Users/yuseonjong/project_exchange/data/01_ARS(아르헨티나)_exchange.csv')
# print(a)