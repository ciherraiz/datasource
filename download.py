from datetime import date
from yahoo import download_yahoo

start_date = date(2002, 1, 1)
end_date = date(2023, 12, 31)


df = download_yahoo(start_date, end_date)
df.to_csv('static/dataset.csv')