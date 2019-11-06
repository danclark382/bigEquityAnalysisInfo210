from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.admin
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)