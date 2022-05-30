from pymongo import MongoClient

host = '35.78.27.97'
port = '27017'
client_aws = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 27017 포트로 들어가서 aws의 DB 와 연결해준다.
client = MongoClient('localhost', 27017)
print(client.list_database_names()) # 현재 데이터베이스 목록 출력
# db_aws = client_aws['exchange']
db = client['interest']
print(db.list_collection_names())
# print(db_aws.list_collection_names())

# for country in db.list_collection_names():
#     data = list(db[country].find({}))
#     db_aws[country].insert_many(data)
#     print(len(list(db_aws[country].find())))


