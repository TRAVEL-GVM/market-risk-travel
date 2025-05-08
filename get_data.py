import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import json
import urllib
import time
from pyjstat import pyjstat
from ecbdata import ecbdata
from fredapi import Fred
from fake_useragent import UserAgent
from datetime import datetime
from config import *
from io import BytesIO
import requests
from io import StringIO



def get_fear_greed_index(start_date='2021-01-01'):

    base_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"
    ua = UserAgent()

    # (YYYY-MM-DD)
    start_date = '2021-01-01'

    headers = {
       'User-Agent': ua.random,
       }

    r = requests.get(base_url + start_date, headers=headers)
    data = r.json()

    data = data['fear_and_greed_historical']

    data_cleaned = [
        {'Date': datetime.utcfromtimestamp(item['x'] / 1000), 'Rating': item['y'], 'Sentiment': item['rating']}
        for item in data['data']
    ]

    df = pd.DataFrame(data_cleaned)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.date

    return df


def get_vix_data(start_date="2020-01-01"):

    df = yf.download("^VIX", start=start_date)

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['Date', 'VIX']
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_yf_data(ticker, start_date="2020-01-01"):

    df = yf.download(ticker, start=start_date)

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['Date', ticker]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def extract_data_from_bank_pt(series_id, variable_name):
    """
    Function to extract data from BPSTAT API.

    Arguments: series_id int
             variable_name str.
             If variable_name is None, variable_name is set to urls label.

    Returns:   pandas dataframe with Date and variable_name columns
    """

    BPSTAT_API_URL = "https://bpstat.bportugal.pt/data/v1"

    url = f"{BPSTAT_API_URL}/series/?lang=EN&series_ids={series_id}"
    series_info = requests.get(url).json()[0]

    domain_id = series_info["domain_ids"][0]
    dataset_id = series_info["dataset_id"]

    dataset_url = f"{BPSTAT_API_URL}/domains/{domain_id}/datasets/{dataset_id}/?lang=EN&series_ids={series_id}"
    dataset = pyjstat.Dataset.read(dataset_url)
    df = dataset.write('dataframe')

    df['Date'] = pd.to_datetime(df['Date'])
    if variable_name is None:
        variable_name = series_info['label']

    df = df.rename(columns={'value': variable_name})
    df = df[['Date', variable_name]]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_bonds_data(country):
    """
    Download and update cds 5y country data, url source example:
    https://pt.investing.com/rates-bonds/germany-5-year-bond-yield-historical-data

    :param country:
    :return: pandas dataframe with bonds 5y data for the country given in the parameter
    """

    path = path_bonds

    df = None

    if country == 'es':
        df = pd.read_csv(path + 'bonds_es_5y.csv').iloc[:, :2]
    elif country == 'pt':
        df = pd.read_csv(path + 'bonds_pt_5y.csv').iloc[:, :2]
    elif country == 'ger':
        df = pd.read_csv(path + 'bonds_ger_5y.csv').iloc[:, :2]
    else:
        print("Fix the written parameter. Countries available: 'es', 'pt', 'ger'.")
        return None

    df.columns = ['Date', 'yield_bonds_5y_' + country]
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y').dt.strftime('%d-%m-%Y')
    df['yield_bonds_5y_' + country] = df['yield_bonds_5y_' + country].str.replace(',', '.').astype(float)

    return df


def get_cds_data(country):
    """
    Download and update cds 5y country data, url source example:
    https://pt.investing.com/rates-bonds/spain-cds-5-years-usd-historical-data

    :param country:
    :return: pandas dataframe with cds 5y data for the country given in the parameter
    """

    path = path_cds

    df = None

    if country == 'es':
        df = pd.read_csv(path + 'cds_es_5y.csv').iloc[:, :2]
    elif country == 'us':
        df = pd.read_csv(path + 'cds_us_5y.csv').iloc[:, :2]
    elif country == 'ger':
        df = pd.read_csv(path + 'cds_ger_5y.csv').iloc[:, :2]
    else:
        print("Fix the written parameter. Countries available: 'es', 'us', 'ger'.")
        return None

    df.columns = ['Date', 'cds_yields_5y_' + country]
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y').dt.strftime('%d-%m-%Y')
    df['cds_yields_5y_' + country] = df['cds_yields_5y_' + country].str.replace(',', '.').astype(float)

    return df


def get_fx_data(from_currency, to_currency, start_date='1900-01-01', api_key=alpha_api_key):
    """
    Function to extract FX rates

    Parameters: api_key: str alpha vantage key (optional)
                from_currency: str
                to_currency: str
                start_date: str YY-MM-DD, if not defined it will retrieve since the beginning

    Returns a pandas DataFrame with Date and FX rates columns
    """

    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_currency}&to_symbol={to_currency}&outputsize=full&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    time_series = data['Time Series FX (Daily)']
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.reset_index()

    df[df.columns[1:]] = df[df.columns[1:]].astype(float)
    df = df.rename(columns={'index': 'Date'})

    df = df[df['Date'] >= start_date]

    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df.iloc[:, :2]
    df.columns = ['Date', from_currency + '_' + to_currency]

    return df


def extract_data_from_ecb(key, start_date='2020-01'):
    """
    Function to extract data from ECB.

    Arguments: key str: URL key
               start_date str:  start date

    Returns:   pandas dataframe with TIME_PERIOD and OBS_VALUE columns
    """

    df = ecbdata.get_series(key,
                            start=start_date, detail='dataonly')

    df.TIME_PERIOD = pd.to_datetime(df.TIME_PERIOD)
    df = df[['TIME_PERIOD', 'OBS_VALUE']]

    return df


def extract_euribor_data_from_ecb(tenor, start_date):
    """
    Function to extract Euribor data.
    Extracted from ECB.
    Returns a dataframe with euribor data for a defined tenor from start_date until now.

    Params:
        - tenor (str): '3M' or '6M' or '1M' or '1Y'
        - startdate (str)

    Returns a dataframe with euribor data for the specified tenor from start_date until now.

    Usage example:  extract_euribor_data_from_ecb('1Y', '2020-01-01')
    """

    dict_keys = {
        '3M': 'FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA',
        '6M': 'FM.M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA',
        '1M': 'FM.M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA',
        '1Y': 'FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA'
    }

    df = extract_data_from_ecb(dict_keys[tenor], start_date)
    df.columns = ['Date', 'Euribor ' + tenor]

    return df


def extract_euribors(start_date):
    """
    Function to extract Euribor data for several tenors ('3M','6M','1M','1Y').
    Extracted from ECB.

    Params:
        - start_date (str)

    Returns a dataframe with euribor data for several tenor from start_date until now.

    Usage example:  extract_euribors('2020-01-01')
    """

    dict_keys = {
        '3M': 'FM.M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA',
        '6M': 'FM.M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA',
        '1M': 'FM.M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA',
        '1Y': 'FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA'
    }

    df_aux = extract_data_from_ecb(dict_keys['1M'], start_date)
    df_aux.columns = ['Date', 'Euribor 1M']

    for tenor in ['3M', '6M', '1Y']:
        df_aux1 = extract_data_from_ecb(dict_keys[tenor], start_date)
        df_aux1.columns = ['Date', 'Euribor ' + tenor]

        df_aux = df_aux.merge(df_aux1, on='Date', how='left')
    df_aux['Date'] = pd.to_datetime(df_aux['Date']).dt.date

    return df_aux


def get_key_ecb_ir(start_year=2015):
    url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.pt.html'

    df = pd.read_html(url)[0].iloc[:-2, :]
    df.columns = ['Ano', 'DiaMes', 'Deposit facility', 'Main refinancing', 'xxx', 'Marginal lending facility']
    df = df.drop(columns=['xxx'])
    df = df.replace({'−': '-', '–': '-'}, regex=True)

    df[['Deposit facility', 'Main refinancing', 'Marginal lending facility']] = df[
        ['Deposit facility', 'Main refinancing', 'Marginal lending facility']].replace('-', float('nan'))

    df[['Deposit facility', 'Main refinancing', 'Marginal lending facility']] = df[
        ['Deposit facility', 'Main refinancing', 'Marginal lending facility']].astype(float)
    df['Ano'] = df['Ano'].replace('-', float('nan'))
    df['Ano'] = df['Ano'].fillna(method='ffill')
    df['Ano'] = df['Ano'].astype(int)

    df['DiaMes'] = df['DiaMes'].str.split('.').str[0]
    df['Date'] = pd.to_datetime(df['Ano'].astype(str) + ' ' + df['DiaMes'], format='%Y %d %b')

    df = df[df['Ano'] >= start_year]
    df = df.drop(columns=['Ano', 'DiaMes'])
    df = df[['Date', 'Deposit facility', 'Main refinancing', 'Marginal lending facility']]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def extract_daily_ts_from_fred(key, obs_column_name, observation_start='2000-01-01', observation_end=None):
    """
    Function to extract a time series from FRED through the url key.

    Params: - url_key: str
            - obs_column_name: str (string you want to the observation value column)
            - observation_start: str (param optional)
            - observation_end: str (param optional)

    Returns: pandas dataframe with column 'Date' and obs_column_name

    extract_daily_ts_from_fred('QPTR628BIS', 're_pt_index', observation_start='2008-01-01', observation_end='2023-12-31')
    """

    fred = Fred(api_key=fred_api_key)

    df = pd.DataFrame(
        fred.get_series(key, observation_start=observation_start, observation_end=observation_end)).reset_index()
    df.columns = ['Date', obs_column_name]

    return df


def extract_data_from_alphavantage(key, api_key=alpha_api_key):
    """
    Function to extract data (US related) from alphavantage website

    Parameters:
        key: str
        api_key: str alphavantage apikey (optional)
        choose one string of the list ['UNEMPLOYMENT', 'CPI', REAL_GDP_PER_CAPITA', 'INFLATION']

    Returns: pandas DataFrame with Date column e key column
    """

    url = f'https://www.alphavantage.co/query?function={key}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = df['value'].astype(float)
    df.columns = ['Date', key]
    # df = df[df['Date'] >= '2020-01-01']
    # df.set_index('Date', inplace=True)

    return df


def get_us_annual_inflation_data(start_date='1900-01-01'):
    df = extract_data_from_alphavantage('Inflation')

    df = df[df['Date'] >= start_date]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_data_bonds_euro_area(start_date='2020-01'):
    df = extract_data_from_ecb('FM.M.U2.EUR.4F.BB.U2_5Y.YLD', start_date=start_date)
    df = df.rename(columns={
        'TIME_PERIOD': 'Date',
        'OBS_VALUE': 'Bonds_euro_area'
    })

    df = df[df['Date'] >= start_date]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_closing_prices(start_date):

    tickers = ['IWDA.AS', '^STOXX50E', '^N100', '^FTSE', 'IVV', 'PSI20.LS']
    df = yf.download(tickers, start=start_date)['Close'].reset_index()
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df.columns = ['Date', 'MSCI World ETF', 'STOXX50E', 'Euronext 100 Index', 'FTSE', 'S&P500 ETF', 'PSI20 Index']
    return df


def get_warren_buffet(start_date='2016-01-01'):
    gdp = extract_daily_ts_from_fred('GDP', 'GDP', observation_start=start_date, observation_end=None)
    gdp['Year_Month'] = gdp['Date'].dt.to_period('M')
    gdp = gdp[['Year_Month', 'GDP']]
    gdp.columns = ['Date', 'GDP']

    market_cap = get_yf_data('^FTW5000', start_date=start_date)
    market_cap['Date'] = pd.to_datetime(market_cap['Date'])
    market_cap['Year_Month'] = market_cap['Date'].dt.to_period('M')
    market_cap_first_day = market_cap.groupby('Year_Month').first().reset_index()
    market_cap_first_day['Year_Month'] = market_cap_first_day['Date'].dt.to_period('M')
    market_cap_first_day = market_cap_first_day[['Year_Month', '^FTW5000']]
    market_cap_first_day.columns = ['Date', 'Marketcap_5000']

    df = pd.merge(gdp, market_cap_first_day, how='left', on='Date')
    df['Indicador de Warren Buffett (%)'] = (df['Marketcap_5000'] / df['GDP']) * 100

    return df


def get_pt_cppi_annual_data(start_year=2000):
    urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CPP/1.0/A.PT.0.A.0.1.6.0?format=csv"]

    df = pd.concat([pd.read_csv(url) for url in urls])[['TIME_PERIOD', 'OBS_VALUE']]
    df.columns = ['Year', 'CPPI PT']
    df = df[df['Year'] >= start_year]

    return df


def get_pt_cppi_annual_data_v2(start_year=2000):
    url = "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CPP/1.0/A.PT.0.A.0.1.6.0?format=csv"

    try:
        # Faz a requisição HTTP com timeout
        response = requests.get(url, timeout=20)
        response.raise_for_status()  # Verifica se houve erro de HTTP
        # Converte o conteúdo da resposta em um DataFrame
        df = pd.read_csv(StringIO(response.text))[['TIME_PERIOD', 'OBS_VALUE']]
        df.columns = ['Year', 'CPPI PT']
        df = df[df['Year'] >= start_year]
        return df

    except requests.exceptions.Timeout:
        print("Timeout occurred while fetching data.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    return None


def get_euroarea18_cppi_annual_data(start_date='2000-01'):
    key = "RESC.Q.I7._T.N._TC.TVAL.4F0.TH.N.IX"
    df = extract_data_from_ecb(key, start_date=start_date)[['TIME_PERIOD', 'OBS_VALUE']]
    df = df[df['TIME_PERIOD'] >= start_date]
    df.columns = ['Date', 'CPPI EURO AREA']
    # df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_residential_property_index_data(start_date='2000-01'):
    key_euro = "RESR.Q.I9._T.N._TR.TVAL.4F0.TB.N.IX"
    key_pt = "RESR.Q.PT._T.N._TR.TVAL.29.TB.N.IX"

    df_euro = extract_data_from_ecb(key_euro, start_date=start_date)[['TIME_PERIOD', 'OBS_VALUE']]
    df_euro = df_euro[df_euro['TIME_PERIOD'] >= start_date]
    df_euro.columns = ['Date', 'HPI EURO AREA']

    df_pt = extract_data_from_ecb(key_pt, start_date=start_date)[['TIME_PERIOD', 'OBS_VALUE']]
    df_pt = df_pt[df_pt['TIME_PERIOD'] >= start_date]
    df_pt.columns = ['Date', 'HPI PT']

    df = df_euro.merge(df_pt, on='Date', how='outer')

    # df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df


def get_exchange_rate_from_yf(currency1, currency2, start_date='2020-01-01', end_date=None):
    """
    Função para obter a taxa de câmbio histórica entre duas moedas.

    Parâmetros:
    - currency1: Código da primeira moeda (ex: 'EUR')
    - currency2: Código da segunda moeda (ex: 'USD')
    - start_date: Data de início no formato 'YYYY-MM-DD'
    - end_date: Data de término no formato 'YYYY-MM-DD'

    Retorna:
    - DataFrame com os dados históricos de taxas de câmbio.
    """
    symbol = f"{currency1}{currency2}=X"

    df = yf.download(symbol, start=start_date, end=end_date)

    df = df.reset_index()[['Date', 'Close']]
    df.columns = ['Date', currency1 + '_' + currency2]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df

def get_all_bonds_data():
    df_bonds_pt = get_bonds_data('pt')
    df_bonds_es = get_bonds_data('es')
    df_bonds_ger = get_bonds_data('ger')

    df_bonds_euro = get_data_bonds_euro_area(start_date='2020-01')

    # Padronizar as datas para o formato YYYY-MM-DD (mesmo que o df_bonds_euro)
    df_bonds_pt['Date'] = pd.to_datetime(df_bonds_pt['Date'], format='%d-%m-%Y')
    df_bonds_es['Date'] = pd.to_datetime(df_bonds_es['Date'], format='%d-%m-%Y')
    df_bonds_ger['Date'] = pd.to_datetime(df_bonds_ger['Date'], format='%d-%m-%Y')
    df_bonds_euro['Date'] = pd.to_datetime(df_bonds_euro['Date'], format='%Y-%m-%d')

    # Renomear as colunas de bond rate para nomes consistentes
    df_bonds_pt = df_bonds_pt.rename(columns={'Bond Rate': 'Bond Rate PT'})
    df_bonds_es = df_bonds_es.rename(columns={'Bond Rate': 'Bond Rate ES'})
    df_bonds_ger = df_bonds_ger.rename(columns={'Bond Rate': 'Bond Rate GER'})
    df_bonds_euro = df_bonds_euro.rename(columns={'Bond Rate': 'Bond Rate Euro'})

    # Combinar os DataFrames usando a coluna 'Date' como chave
    df_combined = pd.merge(df_bonds_pt, df_bonds_es, on='Date', how='outer')
    df_combined = pd.merge(df_combined, df_bonds_ger, on='Date', how='outer')
    df_combined = pd.merge(df_combined, df_bonds_euro, on='Date', how='outer')

    # Ordenar por data, para garantir que as datas estejam na ordem correta
    df_combined = df_combined.sort_values(by='Date').reset_index(drop=True)

    return df_combined


def convert_df_to_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max() + 2, len(col) + 2) # Calcula o tamanho máximo da coluna + padding
            worksheet.set_column(idx, idx, max_len)  # Define a largura de cada coluna

        # Formatar o cabeçalho (linha das colunas)
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'font_color': '#FFFFFF',
            'valign': 'center',
            'align': 'center',
            'fg_color': default_color1,
            'border': 1
        })

        cell_format = workbook.add_format({
            'align': 'center',  # Centraliza horizontalmente
            'valign': 'vcenter',  # Centraliza verticalmente
        })

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        for row_num in range(1, len(df) + 1):
            worksheet.set_row(row_num, None, cell_format)

    output.seek(0)
    return output