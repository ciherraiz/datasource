from datetime import date
import pandas as pd
from yahoo import get_yahoo_close_data, get_yahoo_all_data
from stockcharts import get_stockcharts_data
from features import get_symbol_features


end_date = date.today()

start_year = 2010
start_date = date(start_year, 1, 1)

end_date = date(2023, 12, 31)
end_year = end_date.year

df_spx = get_yahoo_all_data('^SPX', start_date, end_date)
df_y = get_yahoo_close_data(['^VIX'], start_date, end_date)


years =  end_year - start_year + 1
df_sc = get_stockcharts_data(['$NYSI', '$NASI', '$NYMO', '$CPC'], years)


df = df_spx.merge(df_y, how='inner', on='Date')

df = df.merge(df_sc, how='inner', on='Date')

df_f = get_symbol_features(df, 'SPX', start_date, end_date)

df_f.to_csv('static/dataset.csv', sep=';', decimal=',')


