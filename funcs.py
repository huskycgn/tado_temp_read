import datetime
import requests
import mariadb
from cred import *


def get_tempdata(roomid) -> dict:
    def get_tado_secret():

        endpoint = "https://auth.tado.com/oauth/token"

        secparameters = {
            "username": username,
            "password": password,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "password",
        }

        acctoken = requests.post(url=endpoint, params=secparameters).json()
        return acctoken["access_token"]

    token = get_tado_secret()

    headers = {"Authorization": f"Bearer {token}"}

    parameters = {
        "Content-Type": "application/json",
    }

    endpoint_home = f"https://my.tado.com/api/v2/homes/{homeid}/zones/{roomid}/state"

    response = requests.get(url=endpoint_home, params=parameters, headers=headers)

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
    base_url = "https://api.weatherapi.com/v1/current.json?key="
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
