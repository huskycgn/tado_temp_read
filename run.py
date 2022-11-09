from funcs import *
import mariadb

connection = mariadb.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database='temps')

cursor = connection.cursor()

# Tado data

temp_dict = get_tempdata()
time = temp_dict['time']
temp = temp_dict['temp']
humid = temp_dict['humid']

statement = f"INSERT INTO WZ (timestamp, temp, humid) VALUES('{time}', {temp}, {humid});"
print(statement)

cursor.execute(statement)

# Hue data - no humidity

temp_dict = get_hue()
time = temp_dict['time']
temp = temp_dict['temp']
humid = 0

statement = f"INSERT INTO KU (timestamp, temp, humid) VALUES('{time}', {temp}, {humid});"

# commit inserts

connection.commit()
