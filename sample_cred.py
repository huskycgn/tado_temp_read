# tado username
username = "your.mail@example.com"
password = "supersecretpassword"
homeid = 00000  # the tado home-id
db_host = "192.168.1.XX"  # Your mariadb instance
db_port = 3306
db_name = "temps"  # your db name

# dict with human-readable room name, db table and color for matplotlib.
# You need to set those up yourself! ;)
ROOMS = {
    "Kitchen": ["KI", "#5D3891"],
    "Living room": ["LR", "#F99417"],
    "Weather": ["OU", "#F00C0C"],
    "Bedroom": ["BE", "#0307FC"],
    "Bathroom": ["BA", "#2B3499"],
}
db_user = "weatheruser"  # your mariadb user
db_pass = "yourdbpass"
HUE_USER = "kjoB0Pmnwze5LZx38rGkzS7uZ5gjSWIJrUgMmHQR"  # Hue API KEY
HUE_IP = "192.168.1.XX"  # IP of your HUE device.
graph_folder = "/Volumes/home/temps/"  # Where you want the graph .pngs to be stored.
WEATHER_API_KEY = "YourWeatherServiceAPI"
SHELLY_API_KEY = "YourShellyAPI-KEY"
SHELLY_DEVICE_ID = "YourShellyDeviceID"
