import yfinance as yf
import pandas as pd


def get_yahoo_close_data(symbols, start_date, end_date):

    data = yf.download(symbols, start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'),   group_by = 'ticker', progress=False)
    df = pd.DataFrame()

    if len(symbols) == 1:
        df[symbols[0].replace('^', '')] = data['Close']
    else:
        for s in symbols:
            df[s.replace('^', '')] = data[s]['Close']
    
    return df.copy()


def get_yahoo_all_data(symbol, start_date, end_date):
    data = yf.download(symbol, start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'),   group_by = 'ticker', progress=False)
    return data