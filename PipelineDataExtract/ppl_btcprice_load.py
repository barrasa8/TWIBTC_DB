import requests
import mysql.connector
import json
import pandas as pd
from datetime import datetime


# Open the file for reading
with open('../credentials.json', 'r') as f:
    # Read the contents of the file
    contents = json.load(f)

# Get the username and password from the environment variables
username = contents['DB_USER']
password = contents['DB_PASSWORD']
dbname   = contents['DB_NAME']
coingecko_api_root = contents['COINGECKO_API_ROOT']


date='21-03-2023'
api_endpoint = coingecko_api_root+'coins/bitcoin/history?date=[[date]]&localization=false'

#DB connection
mydb = mysql.connector.connect(
  host="localhost",
  user=username,
  password=password,
  database=dbname
)


def get_api_price_history(date,api_endpoint):
    response = requests.get(api_endpoint.replace("[[date]]", date))
    return response.json()

def insert_btc_price_history(currency,date,api_endpoint):
    data =get_api_price_history(date,api_endpoint)
    price = data['market_data']['current_price'][currency]
    df = pd.DataFrame(columns=["date", "price", "currency","api_url"])
    df = df.append({"Date": date, "Price": price, "Currency": currency,"api_url":api_endpoint.replace("[[date]]", date)}, ignore_index=True)
    return df


#data = get_api_price_history(date,api_endpoint)
df = insert_btc_price_history('usd',date,api_endpoint)

test= df["Price"].values[0]

mycursor = mydb.cursor()
sql = "INSERT INTO BTCPrice (date,price,currency,api_url) VALUES (%s,%s,%s,%s)"
#val = (test,)
mycursor.execute(sql, (datetime.strptime(df["Date"].values[0], '%d-%m-%Y').date(),test,df["Currency"].values[0],df["api_url"].values[0],))
mydb.commit()


mydb.close()


