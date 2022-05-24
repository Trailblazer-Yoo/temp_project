from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
db = client['exchange']
db.drop_collection('korea')
