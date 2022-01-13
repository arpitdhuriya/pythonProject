import datetime
from datetime import timedelta
import yfinance as yf
import pymongo as pym

date = input("Insert the date to know the profit loss in past")
while True:
    stock_symbol = input("Insert the stock symbol for data to process")
    if stock_symbol == "END":
        break
    try:
        data = yf.Ticker(f"{stock_symbol}.NS")
        till_date = data.history(start=date, end=datetime.datetime.now().date() + timedelta(days=1))
        myclient = pym.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["stocks"]
        mycol = mydb["history"]
        stocks_list = mycol.find_one({"_id":date})
        for i, row in till_date.iterrows():
            print(f"{i}, Today high: {row['High']}, "
                  f" we need to buy at : {stocks_list['stocks'][stock_symbol]['buy']}")
            if row['High'] > stocks_list['stocks'][stock_symbol]['buy']:
                for j, row2 in till_date.iterrows():
                    if i >= j:
                        continue
                    else:
                        print(f"{j}, Today high: {row2['High']}, "
                              f" we bought at : {stocks_list['stocks'][stock_symbol]['buy']}, "
                              f" Profit/loss: {row2['High'] - stocks_list['stocks'][stock_symbol]['buy']}")
                break

    except Exception as e:
        print("Error ", e)
