from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date
from typing import Optional, List

class Indicator(BaseModel):
    '''
    Garante que o json de resposta seja um dicionário com a chave 'year-month' e 'price'
    '''
    year_month: str = Field(alias='year-month')
    value: float = Field(alias='price')
    
    class Config:
        populate_by_name = True
        #allow_population_by_field_name = True

class Indicators(BaseModel):
    data: List[Indicator] 

class Period(BaseModel):
    '''
    Garante que a data digitada esteja no formato correto
    '''
    start_date: date = Field(alias='start_date')
    end_date: Optional[date] = date.today()
    
    class Config:
        populate_by_name = True