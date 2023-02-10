from funcs import *
import mariadb


# Tado data

temp_dict = get_tempdata()
time = temp_dict['time']
temp = temp_dict['temp']
humid = temp_dict['humid']

statement = f"INSERT INTO WZ (timestamp, temp, humid) VALUES('{time}', {temp}, {humid});"
write_db(statement)

# Hue data - no humidity

temp_dict = get_hue()
time = temp_dict['time']
temp = temp_dict['temp']
humid = 0.00

statement = f"INSERT INTO KU (timestamp, temp, humid) VALUES('{time}', {temp}, {humid});"

write_db(statement)


# Create charts

days = 1

createchart(days * 24)
createchart_month(3)