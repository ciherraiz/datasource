import math
from datetime import datetime, date
import requests
import pandas as pd

def get_stockcharts_data(symbols, years):
    df = pd.DataFrame()
    for s in symbols:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        url = f'https://stockcharts.com/c-sc/sc?s={s}&p=D&yr={years}&mn=0&dy=0&i=t3757734781c&img=text&inspector=yes'

        data = requests.get(url, headers={'user-agent': user_agent}).text
        data = data.split('<pricedata>')[1].replace('</pricedata>', '')

        lines = data.split('|')
        data = []
        for line in lines:
            cols = line.split(' ')

            date = datetime(int(cols[1][0:4]), int(cols[1][4:6]), int(cols[1][6:8]))
            value = float(cols[3])

            if not math.isnan(value):
                data.append({'Date': date, s: value})

        data = pd.DataFrame.from_dict(data)

        if not df.empty:
            df = df.merge(data, how='inner', on='Date')
        else:
            df = data
    
    df.rename(columns={s:s.replace('$','') for s in symbols}, inplace=True)
    df.set_index(['Date'], inplace=True)
    return df.copy()


