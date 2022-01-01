import pymongo as pm
import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from numpy import unique
from matplotlib import pyplot
from numpy import where
# Connection with mongodb
try:
    client = pm.MongoClient('mongodb://localhost:27017/')
    db = client['stock']
    collection = db['balance_sheet']
except Exception as e:
    print(f"Error in connecting the database {e}")
    exit()
cursor = collection.find({})
one_quarter = pd.DataFrame()
columns_quarter = ""
data = list(cursor)
symbols=[]
for stock in data:
    df = pd.read_json(stock['data'])
    columns_quarter = df.iloc[0]
    columns_quarter = [c.replace(' ', '') for c in columns_quarter]
    one_quarter = one_quarter.append(df[1:2])
    symbols.append(stock['_id'])
one_quarter.drop(one_quarter.columns[12], axis=1,inplace=True)
one_quarter.columns = columns_quarter
one_quarter['symbol'] = symbols
one_quarter= one_quarter.dropna()
symbols = one_quarter['symbol']
one_quarter_1 = one_quarter.drop(['PARTICULARS', 'symbol'], axis=1)
model = AffinityPropagation(damping=0.9)
model.fit(one_quarter_1)
Yhat = model.predict(one_quarter_1)
print(len(symbols))

for symbol, cluster in zip(symbols,Yhat):
    print(f"{symbol} {cluster}")

final=pd.DataFrame(symbols)
final['cluster'] =Yhat

for i in Yhat:
    print(final[final['cluster']==i])
