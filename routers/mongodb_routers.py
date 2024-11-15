from fastapi import APIRouter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

router = APIRouter(
    prefix="/mongodb",
)

@router.get("/")
def hello():
    return "Hello, FastAPI!"

@router.get("/status")
def status():
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        return {"status": "Successfully connected to MongoDB!"}
    except Exception as e:
        return {"status": "Failed to connect to MongoDB!", "error": str(e)}