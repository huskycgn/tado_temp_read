import requests
from requests.auth import HTTPDigestAuth
from cred import SHELLY_WEB_USER, SHELLY_WEB_PASS
import datetime



class Room:
    def __init__(self, name, dbtable, ipaddress):
        self.name = name
        self.dbtable = dbtable
        self.ipaddress = ipaddress
        self.temp = self.get_shelly_lan()

    def get_shelly_lan(self):
        try:

            timestamp_iso = datetime.datetime.now()
            timestamp_iso = format(timestamp_iso, "%Y-%m-%d %H:%M:%S")
            timestamp = datetime.datetime.now()
            timestamp = format(timestamp, "%Y%m%dT%H%M")


            base_url = f"http://{self.ipaddress}/rpc/BluTRV.GetStatus?id=200"
            response = requests.get(
                url=base_url, auth=HTTPDigestAuth(SHELLY_WEB_USER, SHELLY_WEB_PASS)
            )
            # response = requests.get(url=base_url)
            json_data = response.json()
            print(json_data)
            # print(json_data["current_C"])
        except:
            return 0
        temp = json_data["current_C"]
        output_dict = {"timestamp_iso": timestamp_iso, "time": timestamp, "temp": temp}
        return output_dict