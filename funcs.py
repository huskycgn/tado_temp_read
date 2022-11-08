import datetime
import mariadb
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


connection = mariadb.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database='temps')

cursor = connection.cursor()

temp_dict = get_tempdata()
time = temp_dict['time']
temp = temp_dict['temp']
humid = temp_dict['humid']


statement = f"INSERT INTO WZ (timestamp, temp, humid) VALUES('{time}', {temp}, {humid});"

print(statement)

cursor.execute(statement)

connection.commit()
