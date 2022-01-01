import yfinance as yf
import pandas as pd
import pymongo as pm
import time
# Connection with mongodb
try:
    client = pm.MongoClient('mongodb://localhost:27017/')
    db = client['stock']
    collection = db['history']
except Exception as e:
    print(f"Error in connecting the database {e}")
    exit()

# get stock info

nifty500 = pd.read_csv('../data/ind_nifty500list.csv')

# get historical market data
for stock_symbol in nifty500['Symbol']:
    try:
        data = yf.Ticker(f"{stock_symbol}.NS")
        print(data.info)
        hist = data.history(period="1y")
        query = {'_id': stock_symbol, 'data': hist.to_json()}
        collection.insert_one(query)
        time.sleep(5)
    except Exception as e:
        print(f"Can not fetch the info {e}")
        time.sleep(5)
