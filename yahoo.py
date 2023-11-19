import yfinance as yf
import pandas as pd


def get_yahoo_data(symbols, start_date, end_date):


    data = yf.download(symbols, start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'),   group_by = 'ticker', progress=False)
    df = pd.DataFrame()
    for s in symbols:
        df[s.replace('^', '')] = data[s]['Close']
    #df = df.add_prefix('SPX_')
    
    #df_vix = yf.download('^VIX', start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'), progress=False)
    #df_vix.rename(columns={'Close': 'VIX_Close'}, inplace=True)

    #df = df.merge(df_vix['VIX_Close'], how='inner', left_index=True, right_index=True)
    
    return df.copy()