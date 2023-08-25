from funcs import *


# Tado data
temp_dict = get_tempdata()
time = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']

statement = f"INSERT INTO WZ (timestamp, timestamp_iso, temp, humid) VALUES('{time}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Shelly data
temp_dict = get_shelly()
time = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']

statement = f"INSERT INTO SZ (timestamp, timestamp_iso, temp, humid) VALUES('{time}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)


# Hue data - no humidity
temp_dict = get_hue()
time = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = 0.00

statement = f"INSERT INTO KU (timestamp, timestamp_iso, temp, humid) VALUES('{time}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Weather data

temp_dict = get_weather()
time = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']
cond = temp_dict['cond']
statement = f"INSERT INTO OU (timestamp, timestamp_iso, temp, humid, weathercond) VALUES('{time}','{timestamp_iso}', {temp}, {humid}, '{cond}');"

write_db(statement)

# Create charts
days = 1

createchart(days * 24)
createchart_month(3)
create_comp_chart(24)
