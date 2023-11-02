from datetime import date
import yfinance as yf
import pandas as pd


start_date = date(2002, 1, 1)
end_date = date(2023, 12, 31)

# YAHOO FINANCE DATASOURCE
yf_symbols = ['^SPX', 'VIX']
df_yf = yf.download(yf_symbols, start = start_date.strftime('%Y-%m-%d'), end = end_date.strftime('%Y-%m-%d'), progress=False)

df_yf.to_csv('dataset.csv')