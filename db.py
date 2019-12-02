import pymongo
import json
import os
import dns
import pandas as pd
import logging


logging.basicConfig(level=logging.DEBUG, filename='stock.log', filemode='w')
LOGGER = logging.getLogger(__name__)
with open("myKeys.json") as jsonFile:
    data = json.load(jsonFile)
    mongoUser = data['keys']['mongoUser']
    mongoPassword = data['keys']['mongoPassword']
PRICE_HISTORY = '.csv'
NEWS_HISTORY = 'NEWS.json'


def getDirList(dir='data'):
    if os.path.exists(dir):
        os.chdir(dir)
        return os.listdir()
    return False

def getFileList(dir):
    return dir+NEWS_HISTORY, dir+PRICE_HISTORY


def convertList(lst):
    convertedL = []
    for i in lst:
        convertedL.append(i)
    return convertedL


def getdocuments(dir):
    fileList = []
    splitFiles = []
    for r, d, f in os.walk(os.getcwd()):
        for i in f:
            if not ('.csv' in i or '.json' in i):
                splitFile = i.split('__')
                fileList.append(splitFile)
    return splitFiles

def checkOS(path):
    if os.path.isfile(os.path.abspath(path)):
        return True
    return False


def getCSV(csv):
    if os.path.isfile(csv):
        df = pd.read_csv(csv)
        dfDict = df.set_index('date').T.to_dict('dict')
        return dfDict

def insertPriceAction(mydb, collection, priceDict):
    mycol = mydb[collection]['priceAction']
    for i, row in enumerate(priceDict.items()):
        date = row[0]
        open = row[1]['open']
        high = row[1]['high']
        low = row[1]['low']
        close = row[1]['close']
        volume = row[1]['volume']
        insertRow = {date: row[1]}
        x = mycol.insert_one(insertRow)
        print(collection + ' Price Documents Stored: ' + str(i))

def getNews(news):
    if os.path.isfile(news):
        with open(news, 'r') as f:
            data = json.load(f)
        return data
    return False


def insertNews(mydb, collection, news):
    mycol = mydb[collection]['news']
    for i, row in enumerate(news.items()):
        insertRow = {row[0]: row[1]}
        x = mycol.insert_one(insertRow)
        print(collection + ' News Documents Stored: ' + str(i))


def insertDocument(mydb, collection, doc):
    """Insert a document into the mydb.collection"""
    fs = gridfs.GridFS(mydb)
    documentIn = fs.put(doc)


def insertdocument(mydb, doc):
    """Insert a document into the mydb.collection"""
    if len(doc) != 3:
        return False
    fs = gridfs.GridFS(mydb)
    try:
        date = doc[2].split('_')[-1]
        documentIn = fs.put(doc, filename=doc[2], date=date)
    except Exception as e:
        return e
    return True


myclient = pymongo.MongoClient(f"mongodb://{mongoUser}:{mongoPassword}@dsci210-shard-00-00-fknts.mongodb.net:27017,dsci210-shard-00-01-fknts.mongodb.net:27017,dsci210-shard-00-02-fknts.mongodb.net:27017/test?ssl=true&replicaSet=dsci210-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = myclient['dbTest']
dirList = getDirList()
for dir in dirList:
    print(dir)
    try:
        os.chdir(dir)
    except NotADirectoryError:
        LOGGER.info(f'ERROR for {dir}')
        continue
    news, csv = getFileList(dir)
    #if csv:
    #    priceDict = getCSV(csv)
    #    if priceDict:
    #        insertPriceAction(mydb, dir, priceDict)
    #if news:
    #    newsDict = getNews(news)
    #    if newsDict:
    #        insertNews(mydb, dir, newsDict)
    docs = getdocuments(dir)
    print(docs)
    os.chdir('..')
