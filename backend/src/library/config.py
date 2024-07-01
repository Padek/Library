from starlette.config import Config
from pymongo import MongoClient
import logging

config = Config("../data/.env")

#Set Log Lvl
LOG_LEVEL = logging.INFO
ENV = "PROD"

# Set up database, MongoDbAtlas
client = MongoClient(config("mongoDB_url"))
db = client.library
books_collection = db.books
users_collection = db.users

# Collection to track the next available ID for books
id_tracker_collection = db.id_tracker

# Ensure the ID tracker has an entry for books
if not id_tracker_collection.find_one({"_id": "book_id"}):
    id_tracker_collection.insert_one({"_id": "book_id", "next_id": 1})