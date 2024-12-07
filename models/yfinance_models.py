from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class StockPrice(BaseModel):
    ticker: str = Field(alias='ticker')
    date: str = Field(alias='year-month')
    price : float = Field(alias='price')
    
    class Config:
        populate_by_name = True
        #allow_population_by_field_name = True

class StockPrices(BaseModel):
    data: List[StockPrice] 

class StockInfo(BaseModel):
    ticker: str
    shortName: str
    longName: str
    city: str
    state: str
    country: str
    website: str
    industry: str
    sector: str
    longBusinessSummary: str
    currency: str
    financialCurrency: str
    
    class Config:
        populate_by_name = True
        #allow_population_by_field_name = True

class StockParams(BaseModel):
    ticker: str
    start : Optional[date] = None
    end : Optional[date] = date.today()
    period : Optional[str] = '5y'

    class Config:
        populate_by_name = True
        #allow_population_by_field_name = True
