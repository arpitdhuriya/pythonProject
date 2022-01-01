import pymongo as pm
import pandas as pd

# Connection with mongodb
x = input("Enter the symbol \n")
print(x)
try:
    client = pm.MongoClient('mongodb://localhost:27017/')
    db = client['stock']
    collection = db['history']
except Exception as e:
    print(f"Error in connecting the database {e}")
    exit()
cursor = collection.find({"_id": x})
df = pd.read_json(list(cursor)[0]['data'])

buy = df.iloc[0]['Open']
print(f"Stock buy at {buy}")
# skipping the week 5 session as we assume that we bought on highest of the week 20 AUg is at 2020 is thursday
df = df[2:]
days_count = 0
previous_week_high_l = []
present_week_high = -1
previous_week_high = buy
total_money = buy
for row in df.iloc:
    days_count = days_count + 1
    if row['High'] > present_week_high:
        present_week_high = row['High']
    previous_week_high_l.append(previous_week_high)
    if days_count == 5:
        previous_week_high = present_week_high
        present_week_high = -1
        days_count = 0
df['previous_week_high'] = previous_week_high_l
print(df[:20])




