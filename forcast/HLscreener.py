import datetime
import yfinance as yf
import pandas as pd
import pymongo as pym
import time


inf = ['../data/ind_niftynext50list.csv','../data/ind_nifty50list.csv','../data/ind_niftymidcap50list.csv', '../data/ind_niftysmallcap50list.csv']
# get historical market data


def hl_screener(history, stock_symbol):
    mid = -1
    up = -1
    down = -1
    low = -1
    ind = 0
    high = -1
    days_count = 0
    for index, day in history.iterrows():
        if ind == 0:
            low = day['Close']
            high = day['High']
            down = day['Low']
            ind = 1
            days_count = days_count + 1
        elif low < day['High'] and high < day['High']:
            up = day['High']
            low = day['Close']
            high = day['High']
            days_count = days_count + 1
        else:
            break
    if up > 0 and days_count >= 2 and ((up - low)/low) > 0.02:
        mid = (down + up)/2
        print(f"stock_symbol {stock_symbol}, buy at {mid}, total days between low {down} and high {up} is {days_count}")
        stocks_data[stock_symbol]={"buy":mid, "down":down, "up":up, "days_count":days_count}
    return mid

stocks_data={}

for nifty_path in inf:
    print(nifty_path[8:-4])
    myclient = pym.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["stocks"]
    mycol = mydb["history"]
    nifty = pd.read_csv(nifty_path)
    for stock_symbol in nifty['Symbol']:
        try:
            data = yf.Ticker(f"{stock_symbol}.NS")
            hist = data.history(period="2mo")
            hist = hist[::-1]
            hl_screener(hist, stock_symbol)
            time.sleep(1)
        except Exception as e:
            print(f"Can not fetch the info {e}")
            time.sleep(5)
try:
    mycol.insert_one({"_id": str(datetime.datetime.now().date()),  "stocks":stocks_data})
    print("Successfully written to the database")
except Exception as e:
    print("can not write to the database %s", e)
