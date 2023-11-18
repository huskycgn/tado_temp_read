from funcs import *
import time
import datetime

# Tado data

# Living room

temp_dict = get_tempdata(1)
time_stamp_legacy = temp_dict["time"]
timestamp_iso = temp_dict["timestamp_iso"]
temp = temp_dict["temp"]
humid = temp_dict["humid"]

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO WZ (time, unixtimestamp, timestamp, time_iso, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Bathroom

temp_dict = get_tempdata(4)
time_stamp_legacy = temp_dict["time"]
timestamp_iso = temp_dict["timestamp_iso"]
temp = temp_dict["temp"]
humid = temp_dict["humid"]

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO BZ (time, unixtimestamp, timestamp, time_iso, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

## Shelly data

# Bathroom

temp_dict = get_shelly()
time_stamp_legacy = temp_dict["time"]
timestamp_iso = temp_dict["timestamp_iso"]
temp = temp_dict["temp"]
humid = temp_dict["humid"]

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO SZ (time, unixtimestamp, timestamp, time_iso, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)


# Hue data - no humidity

# Kitchen

temp_dict = get_hue()
time_stamp_legacy = temp_dict["time"]
timestamp_iso = temp_dict["timestamp_iso"]
temp = temp_dict["temp"]
humid = 0.00

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO KU (time, unixtimestamp, timestamp, time_iso, temp, humid) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}', '{timestamp_iso}', {temp}, {humid});"

write_db(statement)

# Weather data

temp_dict = get_weather()
time_stamp_legacy = temp_dict["time"]
timestamp_iso = temp_dict["timestamp_iso"]
temp = temp_dict["temp"]
humid = temp_dict["humid"]
cond = temp_dict["cond"]

unixtime = time.time()
utcts = datetime.datetime.utcnow()

statement = f"INSERT INTO OU (time, unixtimestamp, timestamp, time_iso, temp, humid, weathercond) VALUES('{utcts}', {unixtime}, '{time_stamp_legacy}','{timestamp_iso}', {temp}, {humid}, '{cond}');"

write_db(statement)

# Create charts
days = 1

createchart(days * 24)
createchart_month(3)
create_comp_chart(24)
