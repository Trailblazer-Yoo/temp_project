from pymongo import MongoClient

client = MongoClient('localhost', 27017)
host = '35.78.27.97'
port = '27017'
client_aws = MongoClient(f'mongodb://{host}:{port}')  # mongoDB는 내 컴퓨터 내의 27017 포트로 들어가서 DB 와 연결해준다.
d =  'interst2'
db = client[d]
db_aws = client_aws['interest']
for country in db.list_collection_names():
    coll = db[country]
    coll_aws = db_aws[country]
    data = list(coll.find({}, {'_id' : 0}))
    coll_aws.insert_many(data)