import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import mariadb
from cred import *


def get_tempdata(roomid) -> dict:
    parameters = {"username": username, "password": password}

    endpoint_home = f"https://my.tado.com/api/v2/homes/{homeid}/zones/{roomid}/state"

    response = requests.get(url=endpoint_home, params=parameters)

    json_data = response.json()

    temp = json_data["sensorDataPoints"]["insideTemperature"]["celsius"]
    humid = json_data["sensorDataPoints"]["humidity"]["percentage"]
    timestamp = datetime.datetime.now()
    timestamp_iso = datetime.datetime.now()
    timestamp = format(timestamp, "%Y%m%dT%H%M")
    timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
    output_dict = {
        "time": timestamp,
        "timestamp_iso": timestamp_iso,
        "temp": temp,
        "humid": humid,
    }
    return output_dict


def get_weather():
    api_key = WEATHER_API_KEY
    city = "cologne"
    base_url = "http://api.weatherapi.com/v1/current.json?key="
    req_url = base_url + api_key + "&q=" + city

    response = requests.get(url=req_url)
    timestamp_iso = datetime.datetime.now()
    timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, "%Y%m%dT%H%M")
    json_data = response.json()
    cond = json_data["current"]["condition"]["text"]
    output_dict = {"timestamp_iso": timestamp_iso, "time": timestamp, "cond": cond}
    temp = float(json_data["current"]["temp_c"])
    humid = float(json_data["current"]["humidity"])
    output_dict["temp"] = temp
    output_dict["humid"] = humid
    return output_dict


def get_shelly():
    api_key = SHELLY_API_KEY
    parameters = {"id": SHELLY_DEVICE_ID, "auth_key": api_key}

    base_url = "https://shelly-77-eu.shelly.cloud/device/status"

    response = requests.get(url=base_url, params=parameters)
    json_data = response.json()
    timestamp_iso = datetime.datetime.now()
    timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, "%Y%m%dT%H%M")
    output_dict = {"timestamp_iso": timestamp_iso, "time": timestamp}
    temp = float(json_data["data"]["device_status"]["temperature:0"]["tC"])
    humid = float(json_data["data"]["device_status"]["humidity:0"]["rh"])
    output_dict["temp"] = temp
    output_dict["humid"] = humid
    return output_dict


def get_hue() -> dict:
    # Temp Sensor has ID 6
    timestamp = datetime.datetime.now()
    timestamp_iso = datetime.datetime.now()
    timestamp = format(timestamp, "%Y%m%dT%H%M")
    timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
    endpoint: str = f"http://{HUE_IP}/api/{HUE_USER}/sensors/6"

    raw_data = requests.get(url=endpoint)

    data = raw_data.json()

    hue_temp = data["state"]["temperature"] / 100

    temp_dict = {
        "time": timestamp,
        "timestamp_iso": timestamp_iso,
        "temp": hue_temp,
    }

    return temp_dict


def write_db(statement: str) -> None:
    """Accepts and executes SQL Statements
    :param statement:
    :return:
    """
    connection = mariadb.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None


def pulldata_db(datapoints: int, room: str) -> pd.DataFrame:
    """Pulls data from DB"""
    connection = mariadb.connect(
        host=db_host, user=db_user, password=db_pass, db=db_name
    )
    statement = f"SELECT timestamp ,temp FROM {room} ORDER BY timestamp DESC LIMIT {int(datapoints)}"
    cursor = connection.cursor()
    cursor.execute(statement)

    data = cursor.fetchall()

    timestamp = []
    temp = []

    for d in data:
        timestamp.append(d[0])
        temp.append(d[1])

    timestamp.reverse()
    temp.reverse()

    newtslist = []

    for ts in timestamp:
        year = ts[0:4]
        month = ts[4:6]
        day = ts[6:8]
        hour = ts[9:11]
        minute = ts[11:13]
        newts = f"{year}-{month}-{day}T{hour}:{minute}"
        newts = np.datetime64(newts)
        newtslist.append(newts)

    # print(temp, newtslist)

    d = {"time": newtslist, "temp": temp}
    df_temp = pd.DataFrame(data=d, index=d["time"])
    return df_temp


def plotgraph(data: object) -> object:
    """returns plot-object"""
    return plt.plot(data, color="#2D033B")


def createchart(hours: int = 36):
    """returns graphs for temperature - expects int as number of desired hours.
    :param hours:
    """
    # Rooms needs to be in the form of:
    # {'room_name': ['table_in_db', '#colorcode'], 'another_room_name': [
    # 'another_table_in_db', '#another_color_code']}
    for r in ROOMS:
        data = pulldata_db(int(hours * (60 / 5)), ROOMS[r][0])
        timestamp = datetime.datetime.now()
        timestamp = format(timestamp, "%Y-%m-%d %H:%M")
        plt.figure(figsize=(15, 10), dpi=300)
        ax = plt.axes()
        ax.set_facecolor("#E5B8F4")
        ax.text(
            0.1,
            0.9,
            f"Mean: {round(float(data.mean(numeric_only=True)), 2)}°C\n"
            f"Max:   {round(float(data.max(numeric_only=True)), 2)}°C\n"
            f"Min:    {round(float(data.min(numeric_only=True)), 2)}°C"
            f"",
            transform=ax.transAxes,
            fontsize=15,
            bbox=dict(alpha=0.2, color="#2D033B"),
        )
        dtFmt = mdates.DateFormatter("%d.%m. - %H:%M")
        plt.gca().xaxis.set_major_formatter(dtFmt)
        # plt.plot(data, color='#2D033B')
        data = data.set_index("time")
        plt.title(
            f"{r} - {hours} Hours Temp\nCreated at: {timestamp}", fontsize=20, pad=20
        )
        plotgraph(data)
        plt.ylabel("Temp °C", fontsize=20)
        plt.grid()
        plt.xticks(rotation=45)
        plt.savefig(f"{graph_folder}{r}.png")
        plt.show()
        plt.close()
    return None


def createchart_month(months: int = 3):
    """returns graphs for temperature - expects int as number of desired hours.
    :param months:
    """
    for r in ROOMS:
        # ROOMS is a dict with the room name as a key and the table name in the db is the value.
        df_temp = pulldata_db(int((round(months * 30 * 24 * 60) / 5)), ROOMS[r][0])
        df_temp_day = df_temp.resample("D", on="time").mean()
        plt.figure(figsize=(15, 10), dpi=300)
        timestamp_print = datetime.datetime.now()
        timestamp_print = format(timestamp_print, "%Y-%m-%d %H:%M")

        ax = plt.axes()
        ax.set_facecolor("#E5B8F4")
        ax.text(
            0.1,
            0.9,
            f"Mean: {round(float(df_temp_day.mean()), 2)}°C\n"
            f"Max:   {round(float(df_temp_day.max()), 2)}°C\n"
            f"Min:    {round(float(df_temp_day.min()), 2)}°C"
            f"",
            transform=ax.transAxes,
            fontsize=15,
            bbox=dict(alpha=0.2, color="#2D033B"),
        )
        dtFmt = mdates.DateFormatter("%d.%m.")
        plt.gca().xaxis.set_major_formatter(dtFmt)
        plotgraph(df_temp_day)
        plt.title(
            f"{r} - {months} Month daily mean Temp\nCreated at: {timestamp_print}",
            fontsize=20,
            pad=20,
        )
        plt.ylabel("Temp °C", fontsize=20)
        plt.grid()
        plt.xticks(rotation=45)
        plt.savefig(f"{graph_folder}{r}_3_Mon.png")
        plt.show()
        plt.close()
    return None


def create_comp_chart(hours: int = 36):
    """returns graphs for temperature for all rooms - expects int as number of desired hours.
    :param hours:
    """
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, "%Y-%m-%d %H:%M")
    plt.figure(figsize=(15, 10), facecolor="#F5F5F5", dpi=300)
    ax = plt.axes()
    ax.set_facecolor("#E8E2E2")
    for r in ROOMS:
        data = pulldata_db(int(hours * (60 / 5)), ROOMS[r][0])
        d = data.set_index("time")
        plt.plot(d, label=r, color=ROOMS[r][1])
    dtFmt = mdates.DateFormatter("%d.%m. - %H:%M")
    plt.gca().xaxis.set_major_formatter(dtFmt)
    plt.title(
        f"All rooms - {hours} Hours Temp\nCreated at: {timestamp}", fontsize=20, pad=20
    )
    plt.ylabel("Temp °C", fontsize=20)
    plt.grid()
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig(f"{graph_folder}temps_all.png")
    plt.show()
    plt.close()
    return None
