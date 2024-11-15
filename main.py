from fastapi import FastAPI
from routers.mongodb_routers import router as mongodb_router

api = FastAPI()
api.include_router(mongodb_router)


@api.get("/")
def read_root():
    return {"message": "API is running!"}
