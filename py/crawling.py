import krx
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.django_test

for day in range(20211101, 20211110):
    df = krx.fundamental_excel(day)
    df['일자'] = str(day)
    df = df.to_dict('index')
    for row in range(len(df)):
        doc = df[row]
        db.fundamental.insert_one(doc)
