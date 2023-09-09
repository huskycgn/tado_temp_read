from funcs import *
import time
import datetime

# Tado data
temp_dict = get_tempdata()
time_stamp_legacy = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO WZ (utc, unixtimestamp, timestamp, time, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Shelly data
temp_dict = get_shelly()
time_stamp_legacy = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO SZ (utc, unixtimestamp, timestamp, time, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)


# Hue data - no humidity
temp_dict = get_hue()
time_stamp_legacy = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = 0.00

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO KU (utc, unixtimestamp, timestamp, time, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Weather data

temp_dict = get_weather()
time_stamp_legacy = temp_dict['time']
timestamp_iso = temp_dict['timestamp_iso']
temp = temp_dict['temp']
humid = temp_dict['humid']
cond = temp_dict['cond']

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO OU (utc, unixtimestamp, timestamp, time, temp, humid, weathercond) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}','{timestamp_iso}', {temp}, {humid}, '{cond}');"

write_db(statement)

# Create charts
days = 1

createchart(days * 24)
createchart_month(3)
create_comp_chart(24)
