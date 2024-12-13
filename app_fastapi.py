from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import PyMongoError  # Use PyMongoError instead of ConnectionError

app = FastAPI()

# MongoDB URI
MONGO_URI = "mongodb://localhost:27017"  # Change to your MongoDB URI

def check_mongo_connection():
    try:
        # Try connecting to the MongoDB server
        client = MongoClient(MONGO_URI)
        # Check if the connection is successful by sending a ping command
        client.admin.command('ping')
        print("MongoDB connected successfully!")
        return True
    except PyMongoError as e:  # Catch all pymongo errors
        print(f"MongoDB connection failed: {e}")
        return False

@app.get("/")
def index():
    if check_mongo_connection():
        return {"message": "MongoDB is connected"}
    else:
        return {"message": "MongoDB connection failed"}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
