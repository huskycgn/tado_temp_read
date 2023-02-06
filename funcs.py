import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import mariadb
from cred import *


def get_tempdata():
    parameters = {
        'username': username,
        'password': password
    }

    endpoint_home = f'https://my.tado.com/api/v2/homes/{homeid}/zones/1/state'

    response = requests.get(url=endpoint_home, params=parameters)

    json_data = (response.json())

    temp = json_data[ 'sensorDataPoints' ][ 'insideTemperature' ][ 'celsius' ]
    humid = json_data[ 'sensorDataPoints' ][ 'humidity' ][ 'percentage' ]
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, '%Y%m%dT%H%M')
    output_dict = { 'time': timestamp, 'temp': temp, 'humid': humid }
    return output_dict


def get_hue():
    # Temp Sensor has ID 6
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, '%Y%m%dT%H%M')
    ENDPOINT = f'http://{HUE_IP}/api/{HUE_USER}/sensors/6'

    raw_data = requests.get(url=ENDPOINT)

    data = raw_data.json()

    hue_temp = data[ 'state' ][ 'temperature' ] / 100

    temp_dict = {
        'time': timestamp,
        'temp': hue_temp,
    }

    return temp_dict


def createchart(hours: int = 36):
    """returns graphs for temperature - expects int as number of desired hours."""
    for r in ROOMS:
        # ROOMS is a dict with the room name as a key and the table name in the db is the value.
        connection = mariadb.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
        statement = f'SELECT * FROM {ROOMS[ r ]} ORDER BY timestamp DESC LIMIT {int((hours*60)/5)}'
        cursor = connection.cursor()
        cursor.execute(statement)

        data = cursor.fetchall()

        timestamp = [ ]
        temp = [ ]

        for d in data:
            timestamp.append(d[ 0 ])
            temp.append(d[ 1 ])

        timestamp.reverse()
        temp.reverse()

        newtslist = [ ]

        for ts in timestamp:
            year = ts[ 0:4 ]
            month = ts[ 4:6 ]
            day = ts[ 6:8 ]
            hour = ts[ 9:11 ]
            minute = ts[ 11:13 ]
            newts = f'{year}-{month}-{day}T{hour}:{minute}'
            newts = np.datetime64(newts)
            newtslist.append(newts)
        plt.figure(figsize=(15, 10))
        timestamp = datetime.datetime.now()
        timestamp = format(timestamp, '%Y-%m-%d %H:%M')
        ax = plt.axes()
        ax.set_facecolor('#E5B8F4')
        dtFmt = mdates.DateFormatter('%d.%m. - %H:%M')
        plt.gca().xaxis.set_major_formatter(dtFmt)
        plt.plot(newtslist, temp, color='#2D033B')
        plt.title(f'{r} - {hours} hours Temp\nCreated at: {timestamp}',  fontsize=20, pad=20)
        # plt.xlabel('Time')
        plt.ylabel('Temp °C', fontsize=20)
        plt.grid()
        plt.xticks(rotation=45)
        # print(f'{ROOMS[ r ]} Max {max(temp)}')
        # print(f'{ROOMS[ r ]} Min {min(temp)}')
        plt.savefig(f'{graph_folder}{ROOMS[ r ]}.png')
        plt.show()
        plt.close()
