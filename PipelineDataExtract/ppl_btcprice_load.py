import os
import requests
import mysql.connector
import json




# Load the credentials file
with open(os.environ['CREDENTIALS_FILE_PATH']) as f:
    credentials = json.load(f)

# Get the username and password from the environment variables
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

mydb = mysql.connector.connect(
  host="localhost",
  user=username,
  password=password,
  database="btc_db"
)

response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
bitcoin_price = response.json()['bitcoin']['usd']


mycursor = mydb.cursor()
sql = "INSERT INTO BTCPrice (price) VALUES (%s)"
val = (bitcoin_price,)
mycursor.execute(sql, val)
mydb.commit()
