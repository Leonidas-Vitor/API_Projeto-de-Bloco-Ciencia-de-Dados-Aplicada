from fastapi import APIRouter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from pydantic import BaseModel, Field
from bson.json_util import dumps
from typing import List, Dict

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

#Retorna a última data de um documento
@router.get("/last")
def GetLastDocument(database: str, collection: str):
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    collection = db[collection]

    #document = list(collection.find().sort([('_id', -1)]).limit(1))[0]
    document = collection.find_one(sort=[('_id', -1)])
    document.pop('_id', None)

    json_data = dumps(document)
    return json_data

#Retorna os tickers de ações
@router.get("/tickers")
def GetTickers():
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Stocks']
    collection = db['Info']

    tickers = list(collection.find())

    tickers = [ticker['ticker'] for ticker in tickers]

    json_data = dumps(tickers)
    return json_data

#Adiciona documentos a uma collection
@router.post("/{database}/{collection}/")
def InsertData(database: str, collection: str, data : str):
    try:
        uri = os.environ.get("MONGODB_URI")
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[database]
        collection = db[collection]

        data = eval(data)
        collection.insert_many(data)

        return dumps({"status": "Data inserted successfully!"})
    except Exception as e:
        return dumps({"status": "Failed to insert data!", "error": str(e), })


#Checa se um documento existe
@router.get("/{database}/{collection}/check")
def CheckDocument(database: str, collection: str, filter: str):
    uri = os.environ.get("MONGODB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[database]
    collection = db[collection]
    filter = eval(filter)
    document = collection.find_one(filter)

    if document:
        return True
    else:
        return False



#------------------------------------------------------------NÃO TESTADO------------------------------------------------------------


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


