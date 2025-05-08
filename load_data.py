import streamlit as st
import yfinance as yf
from viz import *
from get_data import *
from config import *
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

#yfinance
#plotly
#xlsxwriter
#matplotlib
#seaborn
#pyjstat
#ecbdata
#fredapi
#fake_useragent
#hmmlearn


######################## LOAD DATA


def load_data():
    # MARKET BENCHMARKS INDEXS
    df_benchmarks = get_closing_prices(start_date='2020-01-01')
    print("Benchmarks data loaded successfully.")

    # Residential property prices, Portugal, Quarterly vs EURO AREA
    df_hpi = get_residential_property_index_data(start_date='2000-01')
    print("Residential property prices data loaded successfully.")

    # cppi pt anual
    df_cppi_pt = get_pt_cppi_annual_data_v2(start_year=2000)
    print("CPPI Portugal annual data loaded successfully.")

    # cppi euro area 18 quarterly
    df_cppi_euro = get_euroarea18_cppi_annual_data(start_date='2000-01')
    print("CPPI Euro Area annual data loaded successfully.")
    df_aux_cppi = df_cppi_euro.copy()
    print("Processing CPPI Euro Area data...")
    df_aux_cppi['Year'] = df_aux_cppi['Date'].dt.year
    df_aux_cppi = df_aux_cppi.groupby('Year').mean().reset_index().drop(columns=['Date'])
    df_aux_cppi = df_aux_cppi.merge(df_cppi_pt, on='Year', how='outer').dropna()

    # FEAR & GREED INDEX
    df_greed_fear = get_fear_greed_index()
    print("Fear & Greed Index data loaded successfully.")

    # WARREN BUFFET INDEX
    df_warren_buff = get_warren_buffet(start_date='2016-01-01')
    print("Warren Buffet Index data loaded successfully.")
    df_warren_buff['Date'] = df_warren_buff['Date'].dt.to_timestamp()
    df_warren_buff['Date'] = pd.to_datetime(df_warren_buff['Date'])
    # VOLATILITY Index
    df_vix = get_vix_data()
    print("VIX data loaded successfully.")

    # inflation
    df_ipc_pt = extract_data_from_bank_pt(5721524, 'Inflation')
    print("Inflation data loaded successfully.")
    df_ipc_pt['Date'] = pd.to_datetime(df_ipc_pt['Date'])
    df_ipc_pt = df_ipc_pt[df_ipc_pt['Date'] >= '2000-01-01']

    # EURIBOR
    df_eur = extract_euribors('2020-01')

    # FX EUR vs USD
    df_fx_eur_usd = get_exchange_rate_from_yf('EUR', 'USD', start_date='2020-01-01', end_date=None)
    print("EUR/USD exchange rate data loaded successfully.")
    df_fx_eur_gbp = get_exchange_rate_from_yf('EUR', 'GBP', start_date='2020-01-01', end_date=None)
    print("EUR/GBP exchange rate data loaded successfully.")
    df_fx = df_fx_eur_usd.merge(df_fx_eur_gbp, on='Date', how='outer')

    # KEY ECB IR (deposit facility & refinancing)
    df_key_ecb_ir = get_key_ecb_ir(start_year=2015)
    print("Key ECB interest rates data loaded successfully.")

    # IR STR
    df_ir_str = extract_data_from_bank_pt(12559714, 'IR STR') 
    print("Interest rates STR data loaded successfully.")
    df_ir_str['Date'] = pd.to_datetime(df_ir_str['Date'])
    df_ir_str = df_ir_str[df_ir_str['Date'] >= '2000-01-01']

    return df_benchmarks, df_hpi, df_aux_cppi, df_greed_fear, df_warren_buff, df_vix, df_ipc_pt, df_eur, df_fx, df_key_ecb_ir, df_ir_str