#EIA Inventory Data for Natural Gas
import pandas as pd
import json
import requests
import os

url_eia = os.environ.get('EIA_API_NG')
url_database = os.environ.get('LINK_NG_INVENTORY')
token = os.environ.get('PA_API_TOKEN')

#Retrieve natural gas inventory data from EIA website
url = url_eia
resp = requests.get(url)

#Format data into useable json format
data_NG = json.loads(resp.text)

#Make a dataframe
df_NG = pd.DataFrame(data = data_NG['series'][0]['data'], columns=['Date', 'Bcf'] )

#Dates read from api as strings. Convert to datetime
df_NG['Date'] = pd.to_datetime(df_NG['Date'])

#Get most recent datapoint and format date to be same as in database
year = data_NG['series'][0]['data'][0][0][:4]
month = data_NG['series'][0]['data'][0][0][4:6]
day = data_NG['series'][0]['data'][0][0][6:8]
current_date = year + '-' + month + '-' + day

print('EIA Nat Gas Inventory:', data_NG['series'][0]['data'][0][1])
print('EIA Current Date:', current_date)

#Get the last datapoint from database
url = url_database
data = requests.get(url)
inventory = json.loads(data.text)
last_date = inventory[-1]['date']

#Update the database if current_date != last_date
if current_date == last_date:
    print('current_date:', current_date, 'is equal to last_date:', last_date, '- Database not updated')

else:
    headers = {'Authorization': token}

    payload = {
    'date': current_date,
    'ng_inventory': data_NG['series'][0]['data'][0][1],
    }

    resp = requests.post(url, headers=headers, data=payload)
    print(resp)
