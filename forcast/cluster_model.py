import pymongo as pm
import pandas as pd
import matplotlib.pyplot as plt

# Connection with mongodb
x = input("Enter the symbol \n")
print(x)
try:
    client = pm.MongoClient('mongodb://localhost:27017/')
    db = client['stock']
    collection = db['balance_sheet']
except Exception as e:
    print(f"Error in connecting the database {e}")
    exit()
cursor = collection.find({"_id": x})
df = pd.read_json(list(cursor)[0]['data'])
columns = df.iloc[0]
df = df[1:]
df.columns = columns
df.columns = [c.replace(' ', '') for c in df.columns]
print(df.info())
print(pd.to_numeric(df['AdjustedEPS(Rs)']).plot(title="AdjustedEPS(Rs)"))
plt.show()
print(pd.to_numeric(df['NetSales']).plot(title="NetSales"))
plt.show()
print(pd.to_numeric(df['Depreciation']).plot(title="Depreciation"))
plt.show()
print(pd.to_numeric(df['TotalExpenditure']).plot(title="TotalExpenditure"))
plt.show()
print(pd.to_numeric(df['OperatingProfit']).plot(title="OperatingProfit"))
plt.show()
print(pd.to_numeric(df['Interest']).plot(title="Interest"))
plt.show()
print(pd.to_numeric(df['Tax']).plot(title="Tax"))
plt.show()
print("All Done")
