from datetime import date
import pandas as pd
from yahoo import get_yahoo_data
from stockcharts import get_stockcharts_data


end_date = date.today()

start_year = 2002
start_date = date(start_year, 1, 1)

end_date = date(2023, 12, 31)
end_year = end_date.year


df_y = get_yahoo_data(['^SPX', '^VIX'], start_date, end_date)


years =  end_year - start_year + 1
df_sc = get_stockcharts_data(['$NYSI', '$NASI', '$NYMO'], years)

df = df_y.merge(df_sc, how='inner', on='Date')
df.to_csv('static/dataset.csv')


