import os
from pymongo import MongoClient

def connect_db():
    try:
        mongo_uri = os.getenv("MONGO_URI")  # Using .env file for Mongo URI
        client = MongoClient(mongo_uri)
        print("MongoDB connected")
        return client
    except Exception as error:
        print(f"MongoDB connection failed: {error}")
        return None
