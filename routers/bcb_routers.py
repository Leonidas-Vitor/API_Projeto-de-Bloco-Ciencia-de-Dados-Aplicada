import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
import requests
from services import calendar_services
from models.bcb_models import Period, Indicators

router = APIRouter(
    prefix="/bcb",
)

@router.get("/")
def Status():
    '''
    Retorna código 200 se o serviço estiver disponível
    '''
    try:
        return requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados',
                     params={'formato':'json', 'dataInicial':'01/01/2024', 'dataFinal':'02/01/2024'},
                     timeout=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o Banco Central: {str(e)}")

@router.get("/selic", response_model=Indicators)
def GetSelicPrice(period: Period = Depends()):
    try:
        # URL da API do Banco Central para a Selic mensal (Série 432)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"

        response = requests.get(url)
        data = response.json()

        df_selic = pd.DataFrame(data)
        df_selic['data'] = pd.to_datetime(df_selic['data'], format='%d/%m/%Y')
        df_selic['value'] = df_selic['valor'].astype(float)

        df_selic = df_selic[(df_selic['data'].dt.date >= period.start_date) & 
                            (df_selic['data'].dt.date <= period.end_date)]
        df_selic['year-month'] = df_selic['data'].dt.strftime('%Y-%m')

        #Remover o mês incompleto
        try:
            last_date = df_selic['data'].iloc[-1]
            year = last_date.year
            month = last_date.month
            last_day = calendar_services.get_days_in_month(year, month)
            if last_date.day < last_day:
                df_selic = df_selic[df_selic['year-month'] != last_date.strftime('%Y-%m')]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao remover o mês incompleto: {str(e)}")
        
        df_selic.drop(columns=['data','valor'], inplace=True)


        df_selic = df_selic.groupby('year-month').agg({'value':'mean'}).reset_index()
        df_selic['value'] = df_selic['value'].apply(lambda x: x/12) #Passar para valor mensal
        #df_selic.set_index('year-month', inplace=True)

        return {"data": df_selic.to_dict(orient='records')}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Não foi possível retornar o preço da Selic: {str(e)}")


@router.get("/dollar", response_model=Indicators)
def GetDollarPrice(period: Period = Depends()):
    try:
        # URL da API do Banco Central para a cotação mensal do dólar (Série 3695)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.3695/dados?formato=json"

        response = requests.get(url)
        data = response.json()

        df_dolar = pd.DataFrame(data)
        df_dolar['data'] = pd.to_datetime(df_dolar['data'], format='%d/%m/%Y')
        df_dolar['price'] = df_dolar['valor'].astype(float)

        df_dolar = df_dolar[(df_dolar['data'].dt.date >= period.start_date) &
                            (df_dolar['data'].dt.date <= period.end_date)]
        
        df_dolar['year-month'] = df_dolar['data'].dt.strftime('%Y-%m')

        #Remover o mês incompleto
        try:
            last_date = df_dolar['data'].iloc[-1]
            year = last_date.year
            month = last_date.month
            last_day = calendar_services.get_days_in_month(year, month)
            if last_date.day < last_day:
                df_dolar = df_dolar[df_dolar['year-month'] != last_date.strftime('%Y-%m')]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao remover o mês incompleto: {str(e)}")

        df_dolar.drop(columns=['data','valor'], inplace=True)

        #Desnecessário, pois já é um valor mensal da fonte
        #df_dolar = df_dolar.groupby('year-month').agg({'price':'mean'}).reset_index()
        #df_dolar.set_index('year-month', inplace=True)

        return {"data": df_dolar.to_dict(orient='records')}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Não foi possível retornar o preço do dólar: {str(e)}")

@router.get("/ipca", response_model=Indicators)
def GetIpcaPrice(period: Period = Depends()):
    try:
        # URL da API do Banco Central para o IPCA mensal (Série 433)
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

        response = requests.get(url)
        data = response.json()

        df_ipca = pd.DataFrame(data)
        df_ipca['data'] = pd.to_datetime(df_ipca['data'], format='%d/%m/%Y')
        df_ipca['value'] = df_ipca['valor'].astype(float)

        df_ipca = df_ipca[(df_ipca['data'].dt.date >= period.start_date) & 
                            (df_ipca['data'].dt.date <= period.end_date)]
        
        df_ipca['year-month'] = df_ipca['data'].dt.strftime('%Y-%m')

        #Remover o mês incompleto
        try:
            last_date = df_ipca['data'].iloc[-1]
            year = last_date.year
            month = last_date.month
            last_day = calendar_services.get_days_in_month(year, month)
            if last_date.day < last_day:
                df_ipca = df_ipca[df_ipca['year-month'] != last_date.strftime('%Y-%m')]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao remover o mês incompleto: {str(e)}")

        df_ipca.drop(columns=['data','valor'], inplace=True)

        #df_ipca = df_ipca.groupby('year-month').agg({'value':'mean'}).reset_index()
        #df_ipca.set_index('year-month', inplace=True)

        return {"data": df_ipca.to_dict(orient='records')}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Não foi possível retornar o preço do IPCA: {str(e)}")