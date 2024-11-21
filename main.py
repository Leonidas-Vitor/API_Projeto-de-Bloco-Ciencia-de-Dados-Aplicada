from fastapi import FastAPI
from routers.mongodb_routers import router as mongodb_router
from routers.yfinance_routers import router as yfinance_router
import routers.yfinance_routers as y_methods

api = FastAPI()
api.include_router(mongodb_router)
api.include_router(yfinance_router)

#porta do render é por padrão a 10000

@api.get("/")
def read_root():
    return {"message": "API is running!"}


@api.get("/add_stock/{ticker}")
def add_newStock(ticker: str):
    ''' 
        Adiciona uma nova ação a base de dados
    '''
    #return 'ok'
    try:
        return y_methods.GetStockInfo(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))