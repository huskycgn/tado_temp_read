import requests
from cred import username, password, homeid
import datetime

endpoint_general = 'https://my.tado.com/api/v2/me'

parameters = {
    'username': username,
    'password': password
}

# response = requests.get(url=endpoint_general, params=parameters)


endpoint_home = f'https://my.tado.com/api/v2/homes/{homeid}/zones/1/state'

response = requests.get(url=endpoint_home, params=parameters)

json_data = (response.json())

temp = json_data['sensorDataPoints']['insideTemperature']['celsius']
humid = json_data['sensorDataPoints']['humidity']['percentage']
timestamp = datetime.datetime.now()

print(timestamp)
print(temp)
print(humid)