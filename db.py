import pymongo
import json
import dns
import pandas as pd

with open("myKeys.json") as jsonFile:
    data = json.load(jsonFile)
    mongoUser = data['keys']['mongoUser']
    mongoPassword = data['keys']['mongoPass']

myclient = pymongo.MongoClient(f"mongodb://{mongoUser}:{mongoPassword}@dsci210-shard-00-00-fknts.mongodb.net:27017,dsci210-shard-00-01-fknts.mongodb.net:27017,dsci210-shard-00-02-fknts.mongodb.net:27017/test?ssl=true&replicaSet=dsci210-shard-0&authSource=admin&retryWrites=true&w=majority")
FILE_PATH = 'data/AAPL/AAPL.csv'
collectionInstance = FILE_PATH.split('/')[-2]
df = pd.read_csv('data/AAPL/AAPL.csv')
# format = {Date: [Open,High,Low,Close,Adj Close,Volume]}
dfDict = df.set_index('Date').T.to_dict('dict')
myDB = {'AAPL': dfDict}
mydb = myclient['dbTest']
mycol = mydb[collectionInstance]
for row in myDB['AAPL'].items():
    date = row[0]
    open = row[1]['Open']
    high = row[1]['High']
    low = row[1]['Low']
    close = row[1]['Close']
    volume = row[1]['Volume']
    insertRow = {date: row[1]}
    x = mycol.insert_one(insertRow)
    print(x.inserted_id)
