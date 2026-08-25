from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

users = db.users
brands = db.brands
items = db.items

users.create_index("user_id", unique=True)
users.create_index("nickname", unique=True)