import pymongo
import gridfs
import json
import os
import dns
import pandas as pd
import logging
from pprint import pprint


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


def getDocuments(dir):
    fileList = []
    for r, d, f in os.walk(os.path.join(os.getcwd())):
        for i in f:
            if not ('.csv' in i or '.json' in i):
                fileList.append(i.split('__'))
    return fileList


def checkos(path):
    if os.path.isfile(os.path.abspath(path)):
        return True
    return False


def getCSV(csv):
    if os.path.isfile(csv):
        df = pd.read_csv(csv)
        dfDict = df.set_index('date').T.to_dict('dict')
        return dfDict


def insertPriceAction(mydb, collection, priceDict):
    mycol = mydb[collection]['priceHistory']
    for i, row in enumerate(priceDict.items()):
        date = row[0]
        open = row[1]['open']
        high = row[1]['high']
        low = row[1]['low']
        close = row[1]['close']
        volume = row[1]['volume']
        insertRow = {'date': date,
                     'priceData': row[1]}
        x = mycol.insert_one(insertRow)
        print(collection + ' Price Documents Stored: ' + str(i))


def getNews(news):
    company = news.split('NEWS.')[0]
    if os.path.isfile(news):
        with open(news, 'r') as f:
            data = json.load(f)
            newsList = []
            for article in data[company]['newsHeadlines']:
                formattedNews = {'Datetime': article['datetime'],
                                 'Headline': article['headline'],
                                 'Summary': article['summary'],
                                 'Related': article['related'],
                                 'Url': article['url'],
                                 'Source': article['source']
                                 }
                newsList.append(formattedNews)
            return newsList
    return False


def insertNews(mydb, collection, news):
    mycol = mydb[collection]['news']
    x = mycol.insert_one({'Datetime': {str(news['Datetime']): news}})


def insertdocument(mydb, doc):
    """Insert a document into the mydb.collection"""
    filePath = os.path.join(os.getcwd(), '__'.join(doc))
    print(filePath)
    if len(doc) != 3:
        return False
    fs = gridfs.GridFS(mydb)
    try:
        documentIn = fs.put(open(filePath, 'rb'), Ticker=doc[0], Filename=doc[1], Date=doc[2].split('_')[-1], )
        return fs.get(documentIn)
    except Exception as e:
        return e


myclient = pymongo.MongoClient(f"mongodb://{mongoUser}:{mongoPassword}@dsci210-shard-00-00-fknts.mongodb.net:27017,dsci210-shard-00-01-fknts.mongodb.net:27017,dsci210-shard-00-02-fknts.mongodb.net:27017/test?ssl=true&replicaSet=dsci210-shard-0&authSource=admin&retryWrites=true&w=majority")
mydb = myclient['dbTest']
dirList = getDirList()
for dir in dirList:
    try:
        os.chdir(dir)
    except NotADirectoryError:
        LOGGER.info(f'ERROR for {dir}')
        continue
    news, csv = getFileList(dir)
    if csv:
        priceDict = getCSV(csv)
        if priceDict:
            insertPriceAction(mydb, dir, priceDict)
    if news:
        newsList = getNews(news)
        if newsList:
            [insertNews(mydb, dir, i) for i in newsList]
    docList = getDocuments(dir)
    if not docList:
        continue
    docId = [insertdocument(mydb, f) for f in docList]
    os.chdir('..')

