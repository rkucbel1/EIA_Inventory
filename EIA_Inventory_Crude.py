#EIA Inventory Data for Crude
import json
import requests
import os

url_eia = os.environ.get('EIA_API_CRUDE')
url_database = os.environ.get('LINK_OIL_INVENTORY')
token = os.environ.get('PA_API_TOKEN')

#Retrieve crude inventory data from EIA website
url = url_eia
resp = requests.get(url)

#Format data into useable json format
data_crude = json.loads(resp.text)

#Check data in database against latest data from EIA and update if needed
#Most recent datapoint and format date to be same as in database
year = data_crude['series'][0]['data'][0][0][:4]
month = data_crude['series'][0]['data'][0][0][4:6]
day = data_crude['series'][0]['data'][0][0][6:8]
current_date = year + '-' + month + '-' + day

print('EIA crude inventory: ', data_crude['series'][0]['data'][0][1])
print('EIA date: ', current_date)

#Get the last datapoint from database
url = url_database
data = requests.get(url)
inventory = json.loads(data.text)
last_date = inventory[-1]['date']
print('database date: ', last_date)

#Update the database if current_date != last_date
if current_date == last_date:
    print('current_date:', current_date, 'is equal to last_date:', last_date, '- Database not updated')

else:
    headers = {'Authorization': token}

    payload = {
    'date': current_date,
    'oil_inventory': data_crude['series'][0]['data'][0][1],
    }

    resp = requests.post(url, headers=headers, data=payload)
    print(resp)
