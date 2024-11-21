from fastapi import APIRouter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from pydantic import BaseModel, Field
from bson.json_util import dumps

#ResponseModels
class StockPrice(BaseModel):
    name: str = Field(alias='nome')
    age: int = Field(alias='idade')
    
    class Config:
        populate_by_name = True

#------------------------------------------------------------

router = APIRouter(
    prefix="/mongodb",
)

#Status
@router.get("/")
def status():
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        return {"status": "Successfully connected to MongoDB!"}
    except Exception as e:
        return {"status": "Failed to connect to MongoDB!", "error": str(e)}
    
#Listar databases
@router.get("/databases")
def GetDatabases():
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client.list_database_names()

#Listar collections
@router.get("/{database}/collections")
def GetCollections(database: str):
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    return db.list_collection_names()

#Retorna todos os documentos de uma collection
@router.get("/{database}/{collection}/")
def GetCollectionData(database: str, collection: str):
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    collection = db[collection]

    documents = list(collection.find())

    for document in documents:
        document.pop('_id', None)

    json_data = dumps(documents)
    return json_data

#------------------------------------------------------------NÃO TESTADO------------------------------------------------------------

@router.post("/{database}/{collection}/")
def InsertData(database: str, collection: str, data: dict):
    return {"status": "Not implemented yet!"}
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    collection = db[collection]

    collection.insert_one(data)

    return {"status": "Data inserted successfully!"}

@router.delete("/{database}/{collection}/")
def DeleteData(database: str, collection: str, filter: dict):
    return {"status": "Not implemented yet!"}
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    collection = db[collection]

    collection.delete_one(filter)

    return {"status": "Data deleted successfully!"}

#@router.post("/create-user")
#def create_user(newUser: User):
#    return newUser

#def GetCollection(db_name, collection_name):ddwd
#    uri = os.environ.get("MONGODB_URI")
#    client = MongoClient(uri, server_api=ServerApi('1'))
#    db = client[db_name]
#    return db[collection_name]


