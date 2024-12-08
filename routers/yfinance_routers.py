import pandas as pd
import yfinance as yf
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.yfinance_models import StockPrices, StockInfo, StockParams
from services import calendar_services

router = APIRouter(
    prefix="/yfinance",
)

@router.get("/")
def Status():
    '''
    Retorna código 202 se o serviço estiver disponível
    '''
    try:
        test_ticker = yf.Ticker("AAPL")
        data = test_ticker.history(period="1d")
        return not data.empty
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o Banco Central: {str(e)}")


@router.get("/stock-monthly-price", response_model=StockPrices)
def GetStockData(stockParams: StockParams = Depends()):
    ticker = yf.Ticker(stockParams.ticker)
    if stockParams.start is not None:
        history = ticker.history(start = stockParams.start, end = stockParams.end)
    else:
        history = ticker.history(period=stockParams.period)

    if not history.empty:
        # Remover informações de fuso horário, se existirem
        if history.index.tz is not None:
            history.index = history.index.tz_localize(None)
        history['year-month'] = history.index.to_period('M').strftime('%Y-%m')

        #Remover o mês incompleto, se existir
        last_date = history.index[-1]
        year = last_date.year
        month = last_date.month
        last_day = calendar_services.get_days_in_month(year, month)
        if last_date.day < last_day:
            history = history[history['year-month'] != last_date.strftime('%Y-%m')]

        media_mensal = history.groupby('year-month')['Close'].mean()
        media_mensal = pd.DataFrame(media_mensal)
        media_mensal['ticker'] = stockParams.ticker
        media_mensal = media_mensal.rename(columns={'Close': 'price'})
        media_mensal.sort_index(inplace=True)

        # Converta o DataFrame para uma lista de dicionários para evitar problemas de serialização
        return {'data':media_mensal.reset_index().to_dict(orient='records')}
    else:
        raise HTTPException(status_code=404, detail=f"Ação não encontrada {stockParams.ticker}")

@router.get("/stock-info", response_model=StockInfo)
def GetStockInfo(ticker : str):
    infosToGet = ['shortName','longName','city','state','country','website','industry',
         'sector','longBusinessSummary','currency','financialCurrency']
    try:
        stock = yf.Ticker(ticker)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ação não encontrada {ticker}")
    
    stock_info = {}
    stock_info['ticker'] = ticker
    stock_info.update({key: stock.info.get(key, 'Não disponível') for key in infosToGet})
    #stock_info = stock_info[['ticker', 'shortName', 'longName', 'city', 'state', 'country', 'website', 'industry', 'sector', 'longBusinessSummary', 'currency', 'financialCurrency']]
    return pd.DataFrame(stock_info, index=[0]).to_dict(orient='records')[0]


#ticker.get_recommendations(proxy=None, as_dict=False)
#Returns a DataFrame with the recommendations Columns: period strongBuy buy hold sell strongSell

