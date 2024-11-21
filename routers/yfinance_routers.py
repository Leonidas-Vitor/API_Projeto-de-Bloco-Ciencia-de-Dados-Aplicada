from pydantic import BaseModel, Field
import pandas as pd
import yfinance as yf
from fastapi import APIRouter


#ResponseModels
class StockPrice(BaseModel):
    name: str = Field(alias='nome')
    age: int = Field(alias='idade')
    
    class Config:
        populate_by_name = True

#------------------------------------------------------------

router = APIRouter(
    prefix="/yfinance",
)

@router.get("/stock-monthly-price/{stock_ticker}/")
def GetStockData(stock_ticker, period='5y'):
    acao = yf.Ticker(stock_ticker)
    historico = acao.history(period=period)

    if not historico.empty:
        # Remover informações de fuso horário, se existirem
        if historico.index.tz is not None:
            historico.index = historico.index.tz_localize(None)
        historico['Month'] = historico.index.to_period('M')

        media_mensal = historico.groupby('Month')['Close'].mean()
        media_mensal = pd.DataFrame(media_mensal)
        media_mensal['Ticker'] = stock_ticker
        media_mensal = media_mensal.rename(columns={'Close': 'CloseMean'})
        media_mensal.sort_index(inplace=True)

        # Converta o DataFrame para uma lista de dicionários para evitar problemas de serialização
        return media_mensal.reset_index().to_dict(orient='records')
    else:
        print(f"Não foi possível coletar dados para a ação {stock_ticker}")
        return []

@router.get("/stock-info/{stock_ticker}/")
def GetStockInfo(stock_ticker):
    infosToGet = ['shortName','longName','city','state','country','website','industry',
         'sector','longBusinessSummary','currency','financialCurrency']
    try:
        stock = yf.Ticker(stock_ticker)
    except Exception as e:
        stock = None
    if stock is None:
        print(f"Não foi possível coletar informações para a ação {stock_ticker}")
        return pd.DataFrame()#{key: 'Não disponível' for key in infosToGet}
    stock_info = {}
    stock_info['ticker'] = stock_ticker
    stock_info.update({key: stock.info.get(key, 'Não disponível') for key in infosToGet})
    #stock_info = stock_i[['ticker', 'shortName', 'longName', 'city', 'state', 'country', 'website', 'industry', 'sector', 'longBusinessSummary', 'currency', 'financialCurrency']]
    return pd.DataFrame(stock_info, index=[0])#.to_dict(orient='records')
