import yfinance as yf
import pandas as pd


def download_yahoo(start_date, end_date):
    df = yf.download('^SPX', start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'), progress=False)
    df = df.add_prefix('SPX_')
    
    df_vix = yf.download('^VIX', start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'), progress=False)
    df_vix.rename(columns={'Close': 'VIX_Close'}, inplace=True)

    df = df.merge(df_vix['VIX_Close'], how='inner', left_index=True, right_index=True)
    
    return df.copy()