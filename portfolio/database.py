
# from pymongo import MongoClient
#
# client = MongoClient("mongodb://localhost:27017/")
#
# db = client["contact_database"]
#
# messages_collection = db["messages"]
#
# print(db.list_collection_names())


import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_URL")

client = MongoClient(mongo_url)

db = client["contact_database"]

messages_collection = db["messages"]

print(db.list_collection_names())