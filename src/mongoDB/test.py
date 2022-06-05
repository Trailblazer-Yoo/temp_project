from pymongo import MongoClient

host = '35.78.27.97'
port = '27017'
client_aws = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 27017 포트로 들어가서 aws의 DB 와 연결해준다.
client = MongoClient('localhost', 27017)
db = client['exchange']
db_aws = client_aws['exchange']
print(client_aws.list_database_names())
print(db.list_collection_names())
for country in db.list_collection_names():
    print(country)
    data = list(db[country].find({}))
    db_aws[country].insert_many(data)
print(db_aws.list_collection_names())



