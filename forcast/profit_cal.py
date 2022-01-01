import datetime
import yfinance as yf
import pymongo as pym

date = input("Insert the date to know the profit loss in past")
stock_symbol = input("Insert the stock symbol for data to process")
try:
    data = yf.Ticker(f"{stock_symbol}.NS")
    till_date = data.history(start=date, end=datetime.datetime.now().date())
    myclient = pym.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["stocks"]
    mycol = mydb["history"]
    stocks_list = mycol.find_one({"_id":date})
    for i, row in till_date.iterrows():
        print(i, row['High'], stocks_list['stocks'][stock_symbol]['buy'])
        if row['High'] > stocks_list['stocks'][stock_symbol]['buy']:
            for j, row2 in till_date.iterrows():
                if i >= j:
                    continue
                else:
                    print(j, row2['High'],stocks_list['stocks'][stock_symbol]['buy'],
                          row2['High'] - stocks_list['stocks'][stock_symbol]['buy'])
            break

except Exception as e:
    print("Error %s", e)
