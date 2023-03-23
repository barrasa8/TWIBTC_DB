import os
import requests
import mysql.connector
import json
import pandas as pd
from datetime import datetime,timedelta
import time

#Change directory to executed file directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Open the file for reading
with open('../credentials.json', 'r') as f:
    # Read the contents of the file
    contents = json.load(f)

# Get the username and password from the environment variables
username = contents['DB_USER']
password = contents['DB_PASSWORD']
dbname   = contents['DB_NAME']
alphavantage_api_key = contents['ALPHAVANTAGE_API_KEY']
alphavantage_api_root = contents['ALPHAVANTAGE_API_ROOT']

#DB connection
mydb = mysql.connector.connect(
  host="localhost",
  user=username,
  password=password,
  database=dbname
)

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = alphavantage_api_root+'function=FX_DAILY&outputsize=compact&from_symbol=AUD&to_symbol=USD&apikey='+alphavantage_api_key
r = requests.get(url)
data = r.json()

print(data)