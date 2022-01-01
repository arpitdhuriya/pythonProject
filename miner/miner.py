import pandas as pd
import pymongo as pm
import urllib.request as req
from bs4 import BeautifulSoup
import logging
import time
# Connection with mongodb
try:
    client = pm.MongoClient('mongodb://localhost:27017/')
    db = client['stock']
    collection = db['balance_sheet']
except Exception as e:
    print(f"Error in connecting the database {e}")
    exit()
# List of all the index
nifty500 = pd.read_csv('../data/ind_nifty500list.csv')
for symbol in nifty500['Symbol']:
    # specify the URL
    print(f"Getting data for {symbol}")
    try:
        webpage = 'https://ticker.finology.in/company/'+symbol
        print(webpage)
        page = req.urlopen(webpage)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find('div', attrs={'id': 'mainContent_quarterly'})
        table = name_box.find(attrs={'table'})
        table_rows = table.find_all('tr')
        rows = []
        for tr in table_rows:
            td = tr.find_all(['th', 'td'])
            row = [tr.text for tr in td]
            rows.append(row)
        df = pd.DataFrame(rows)
        df = df.T
        query = {'_id': symbol, 'data': df.to_json()}
        collection.insert_one(query)
        print(f"saving data for {symbol} is done")
        time.sleep(5.0)
    except Exception as e:
        print(f"Error can not fetch the data {e}")
print("Done Fetching the data")
