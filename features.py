from datetime import timedelta
import math
import pandas as pd
from yahoo import get_yahoo_all_data


def get_symbol_features(data, s, start_date, end_date):

    df = pd.DataFrame()
    
    df = data.copy()
    df = df.rename(columns={'Close':s})


    df[s + '_C_O_pct'] = (data['Open'] - data['Close'].shift(1)) / data['Close'].shift(1) #Overnight percentage movement
    df[s + '_O_C_pct'] = (data['Close'] - data['Open']) / data['Open'] #Intraday percentage movement
    #df[s + '_PC_C_pct'] = (data['Close'] - data['Close'].shift(1)) / data['Close'].shift(1) #Close to Close percentage movement
    df[s + '_C_C_pct'] = data['Close'].pct_change() #Close to Close percentage movement
    # Previous Close  to Close percentaje
    df[s + '_P_C_C_pct'] = df[s + '_C_C_pct'].shift()
    
    df[s + '_std'] = data['Close'].rolling(30).std(ddof=0)
    # Standard Deviation expected moves percentage
    df[s + '_PC_1std_pct'] = df[s + '_std'].shift(1) / data['Close'].shift(1)
    df[s + '_PC_2std_pct'] = 2 * df[s + '_std'].shift(1) / data['Close'].shift(1)

    # https://pepperstone.com/en-af/trading/instruments/vix/
    # VIX index = 20% (annualised move in the S&P 500)
    # Square root of time = 15.9 (SQRT/252)
    # Daily move = 1.25% (20/15.9 = 1.25).
    # To get the weekly implied move, we divide 20 by 7.07 
    # (7.07 being the – i.e. there are 50 trading weeks in a year)
    sqrt_time = math.sqrt(252)
    # VIX excepted move percentage
    df[s + '_VEM'] = (df['VIX'] / sqrt_time) / 100 * df[s]
    df[s + '_PC_1VEM_pct'] = df[s + '_VEM'].shift(1) / data['Close'].shift(1)
    df[s + '_PC_2VEM_pct'] = 2 * df[s + '_VEM'].shift(1) / data['Close'].shift(1)


    # Consecutives positive returns
    df['Bool'] = df[s + '_C_C_pct'] > 0
    df[s + '_PC_C_UP_con'] = df['Bool'].groupby((~df['Bool']).cumsum()).cumsum()

    df['Bool'] = df[s + '_O_C_pct'] > 0
    df[s + '_O_C_UP_con'] = df['Bool'].groupby((~df['Bool']).cumsum()).cumsum()

    #df.dropna(inplace=True)


    #seasonality(df, s)

    # Labels
    
    df[s + '_C_C_lbl'] = (df[s + '_C_C_pct'] > 0).astype(int)
    df[s + '_O_C_lbl'] = (df[s + '_O_C_pct'] > 0).astype(int)
    
    df[s + '_PC_C_1std_lbl'] = (df[s + '_PC_1std_pct'] < df[s + '_C_C_pct']).astype(int)
    df[s + '_PC_C_2std_lbl'] = (df[s + '_PC_2std_pct'] < df[s + '_C_C_pct']).astype(int)

    df[s + '_PC_C_1VEM_lbl'] = (df[s + '_PC_1VEM_pct'] < df[s + '_C_C_pct']).astype(int)
    df[s + '_PC_C_2VEM_lbl'] = (df[s + '_PC_2VEM_pct'] < df[s + '_C_C_pct']).astype(int)

    df.drop(columns=['Bool'], inplace=True)
    df.dropna(inplace=True)
    
    return df


def seasonality(data, s):
    start_date = "1990-01-01"
    end_date   = "2022-12-31"
    
    max_date = data.index.max() - timedelta(days=365)
    print(data.tail())
    print(max_date)

    df = pd.DataFrame()
    df['Return'] = data[s + '_PC_C_pct']
    df['Year'] = df.index.year
    df['DayOfYear'] = df.index.dayofyear    
    average_by_day = df.groupby(['DayOfYear', 'Year'])['Return'].mean().reset_index()
    overall_average = average_by_day.groupby('DayOfYear')['Return'].mean().reset_index()
    overall_average['Cumulative Return'] = (1 + overall_average['Return']).cumprod()

    #print(overall_average['Seasonality CR'])

    """
    #sp500_data['Return'] = sp500_data['Close'].pct_change()    
    sp500_data['Year'] = sp500_data.index.year
    sp500_data['DayOfYear'] = sp500_data.index.dayofyear    
    average_sp500_by_day = sp500_data.groupby(['DayOfYear', 'Year'])['Return'].mean().reset_index()
    overall_average_sp500 = average_sp500_by_day.groupby('DayOfYear')['Return'].mean().reset_index()
    overall_average_sp500['Cumulative Return'] = (1 + overall_average_sp500['Return']).cumprod()

    """
