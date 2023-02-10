import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
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


def write_db(statement: str):
    """Accepts and executes SQL Statements"""
    connection = mariadb.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database='temps')

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()


def pulldata_db(datapoints: int, room: str):
    """Pulls data from DB"""
    connection = mariadb.connect(host=db_host, user=db_user, password=db_pass, db=db_name)
    statement = f'SELECT * FROM {ROOMS[ room ]} ORDER BY timestamp DESC LIMIT {int(datapoints)}'
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

    # print(temp, newtslist)

    d = { 'time': newtslist, 'temp': temp }
    df_temp = pd.DataFrame(data=d, index=d[ 'time' ])
    return df_temp


def plotgraph(data):
    return plt.plot(data, color='#2D033B')


def createchart(hours: int = 36):
    """returns graphs for temperature - expects int as number of desired hours."""
    for r in ROOMS:
        data = pulldata_db(hours * (60 / 5), r)
        print(data)
        timestamp = datetime.datetime.now()
        timestamp = format(timestamp, '%Y-%m-%d %H:%M')
        plt.figure(figsize=(15, 10))
        ax = plt.axes()
        ax.set_facecolor('#E5B8F4')
        ax.text(0.1, 0.9, f'Mean: {round(float(data.mean(numeric_only=True)), 2)}°C\n'
                          f'Max:   {round(float(data.max(numeric_only=True)), 2)}°C\n'
                          f'Min:    {round(float(data.min(numeric_only=True)), 2)}°C'
                          f'', transform=ax.transAxes, fontsize=15, bbox=dict(alpha=0.2, color='#2D033B'))
        dtFmt = mdates.DateFormatter('%d.%m. - %H:%M')
        plt.gca().xaxis.set_major_formatter(dtFmt)
        # plt.plot(data, color='#2D033B')
        data = data.set_index('time')
        plt.title(f'{r} - {hours} Hours Temp\nCreated at: {timestamp}', fontsize=20, pad=20)
        plotgraph(data)
        plt.ylabel('Temp °C', fontsize=20)
        plt.grid()
        plt.xticks(rotation=45)
        plt.savefig(f'{graph_folder}{r}.png')
        plt.show()
        plt.close()


def createchart_month(months: int = 3):
    """returns graphs for temperature - expects int as number of desired hours."""
    for r in ROOMS:
        # ROOMS is a dict with the room name as a key and the table name in the db is the value.
        df_temp = pulldata_db((round(months * 30 * 24 * 60) / 5), r)
        df_temp_day = df_temp.resample('D', on='time').mean()
        plt.figure(figsize=(15, 10))
        timestamp_print = datetime.datetime.now()
        timestamp_print = format(timestamp_print, '%Y-%m-%d %H:%M')

        ax = plt.axes()
        ax.set_facecolor('#E5B8F4')
        ax.text(0.1, 0.9, f'Mean: {round(float(df_temp_day.mean()), 2)}°C\n'
                          f'Max:   {round(float(df_temp_day.max()), 2)}°C\n'
                          f'Min:    {round(float(df_temp_day.min()), 2)}°C'
                          f'', transform=ax.transAxes, fontsize=15, bbox=dict(alpha=0.2, color='#2D033B'))
        dtFmt = mdates.DateFormatter('%d.%m.')
        plt.gca().xaxis.set_major_formatter(dtFmt)
        plotgraph(df_temp_day)
        plt.title(f'{r} - {months} Month daily mean Temp\nCreated at: {timestamp_print}', fontsize=20, pad=20)
        plt.ylabel('Temp °C', fontsize=20)
        plt.grid()
        plt.xticks(rotation=45)
        plt.savefig(f'{graph_folder}{r}_3_Mon.png')
        plt.show()
        plt.close()
