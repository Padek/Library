from motor.motor_asyncio import AsyncIOMotorClient
from starlette.config import Config

config = Config("../data/.env")


#set up database, MongoDbAtlas
client = AsyncIOMotorClient(config("mongoDB_url"))
db = client.library
books_collection = db.books