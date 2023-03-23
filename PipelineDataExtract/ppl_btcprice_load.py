import requests
import mysql.connector
import json
import pandas as pd
from datetime import datetime,timedelta
import time


# Open the file for reading
with open('../credentials.json', 'r') as f:
    # Read the contents of the file
    contents = json.load(f)

# Get the username and password from the environment variables
username = contents['DB_USER']
password = contents['DB_PASSWORD']
dbname   = contents['DB_NAME']
coingecko_api_root = contents['COINGECKO_API_ROOT']


startDate='01-03-2022'
dateStr = '01-03-2022' 
date =datetime.strptime(startDate, '%d-%m-%Y')

today=datetime.today().date()

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

def price_history_to_df(currency,date,api_endpoint):
    data =get_api_price_history(date,api_endpoint)
    price = data['market_data']['current_price'][currency]
    df = pd.DataFrame(columns=["date", "price", "currency","api_url"])
    df = df.append({"date": date, "price": price, "currency": currency,"api_url":api_endpoint.replace("[[date]]", date)}, ignore_index=True)
    return df


DayCount = today - datetime.strptime(startDate, '%d-%m-%Y').date()  
DayCount = int(DayCount.total_seconds())/86400
i=0

mycursor = mydb.cursor()


  
while i < int(DayCount):
    print('hello')
    df = price_history_to_df('usd',dateStr,api_endpoint)

    sql = "INSERT INTO BTCPrice (date,price,currency,api_url) VALUES (%s,%s,%s,%s)"
    #val = (test,)
    mycursor.execute(sql, (datetime.strptime(df["date"].values[0], '%d-%m-%Y').date(),df["price"].values[0],df["currency"].values[0],df["api_url"].values[0],))
    mydb.commit()
    
    i += 1
    date= date  + timedelta(days=1)
    dateStr = date.strftime('%d-%m-%Y')
    time.sleep(30)

mydb.close()






