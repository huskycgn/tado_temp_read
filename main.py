import requests
from cred import username, password
import datetime

endpoint_general = 'https://my.tado.com/api/v2/me'

parameters = {
    'username': username,
    'password': password
}

# response = requests.get(url=endpoint_general, params=parameters)


endpoint_home = 'https://my.tado.com/api/v2/homes/592322/zones/1/state'

response = requests.get(url=endpoint_home, params=parameters)

json_data = (response.json())

temp = json_data['sensorDataPoints']['insideTemperature']['celsius']
humid = json_data['sensorDataPoints']['humidity']['percentage']
timestamp = datetime.datetime.now()

print(timestamp)
print(temp)
print(humid)