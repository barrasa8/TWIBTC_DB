import os
import requests
import mysql.connector
import json


# Open the file for reading
with open('../credentials.json', 'r') as f:
    # Read the contents of the file
    contents = json.load(f)

# Get the username and password from the environment variables
username = contents['DB_USER']
password = contents['DB_PASSWORD']
dbname   = contents['DB_NAME']


mydb = mysql.connector.connect(
  host="localhost",
  user=username,
  password=password,
  database=dbname
)

response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
bitcoin_price = response.json()['bitcoin']['usd']


mycursor = mydb.cursor()
sql = "INSERT INTO BTCPrice (price) VALUES (%s)"
val = (bitcoin_price,)
mycursor.execute(sql, val)
mydb.commit()
