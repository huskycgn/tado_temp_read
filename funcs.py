import datetime
import requests
import psycopg2
from cred import *


def get_timestamp_utc():
    return str(datetime.datetime.now(datetime.timezone.utc)).replace("+00:00", "")


def get_tempdata(roomid) -> dict:
    def tado_key_handler():
        with open("refresh_token.txt", "r") as f:
            refresh_token_old = f.readline()

        token = requests.post(
            "https://login.tado.com/oauth2/token",
            params=dict(
                client_id="1bb50063-6b0c-4d11-bd99-387f4a91cc46",
                grant_type="refresh_token",
                refresh_token=refresh_token_old,
            ),
        ).json()

        # print(token)

        access_token = token["access_token"]
        refresh_token = token["refresh_token"]

        # print(access_token)
        # print(refresh_token)

        with open("token.txt", "w") as f:
            f.write(token["access_token"])

        with open("refresh_token.txt", "w") as f:
            f.write(token["refresh_token"])

        # print(access_token, refresh_token)

        return access_token, refresh_token

    token = tado_key_handler()[0]

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
    precipitation = float(json_data["current"]["precip_mm"])
    output_dict["temp"] = temp
    output_dict["humid"] = humid
    output_dict["precipitation"] = precipitation
    return output_dict


def get_shelly():
    api_key = SHELLY_API_KEY
    parameters = {"id": SHELLY_DEVICE_ID, "auth_key": api_key}

    base_url = "https://shelly-226-eu.shelly.cloud/device/status"

    response = requests.get(url=base_url, params=parameters)
    json_data = response.json()
    timestamp_iso = datetime.datetime.now()
    timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
    timestamp = datetime.datetime.now()
    timestamp = format(timestamp, "%Y%m%dT%H%M")
    output_dict = {"timestamp_iso": timestamp_iso, "time": timestamp}
    # print(json_data)
    print(json_data["isok"])
    if json_data["isok"] is False:
        return False
    else:
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
    connection = psycopg2.connect(
        host=db_host, user=db_user, password=db_pass, database=db_name
    )

    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    return None


# thank you tado for making this even more complicated!

print(get_shelly())
