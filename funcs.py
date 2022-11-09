import datetime
import requests

from cred import *


def get_tempdata():
    parameters = {
        'username': username,
        'password': password
    }

    endpoint_home = f'https://my.tado.com/api/v2/homes/{homeid}/zones/1/state'

    response = requests.get(url=endpoint_home, params=parameters)

    json_data = (response.json())

    temp = json_data['sensorDataPoints']['insideTemperature']['celsius']
    humid = json_data['sensorDataPoints']['humidity']['percentage']
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, '%Y%m%dT%H%M')
    output_dict = {'time': timestamp, 'temp': temp, 'humid': humid}
    return output_dict


def get_hue():
    # Temp Sensor has ID 6
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, '%Y%m%dT%H%M')
    ENDPOINT = f'http://192.168.178.41/api/{HUE_USER}/sensors/6'

    raw_data = requests.get(url=ENDPOINT)

    data = raw_data.json()

    hue_temp = data['state']['temperature'] / 100

    temp_dict = {
        'time': timestamp,
        'temp': hue_temp,
    }

    return temp_dict



