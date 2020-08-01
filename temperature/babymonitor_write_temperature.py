from csv import writer
from datetime import datetime
import random
import time
import Adafruit_DHT
import pandas as pd

sensor = 22     # sensor DHT22 (alternatives 11 (DHT11), 2302 (DHT.AM2302))
pin = 4         # GPIO Pin used for signal-
wait_time = 30  # write every 30 seconds new temperature to csv
max_lines = 2000 # max number of lines in csv

def append_list_as_row(filename, list):
	csv = pd.read_csv(filename, sep=",")
	if len(csv) > max_lines:
		csv = csv.drop(csv.index[0])
	csv = csv.append(list, ignore_index=True)
	csv.to_csv(filename,index=False)
	
	#with open(filename, 'a+') as write_obj:
	#	csv_writer = writer(write_obj)
	#	csv_writer.writerow(list)

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
	temperature = round(temperature,2)
	humidity = round(humidity,2)		
	now = datetime.now()
	current_time = now.strftime("%d.%m.%Y-%H:%M:%S")
	#new_row = [current_time, temperature, humidity]
	new_row = {'date': current_time, 'temperature': temperature, 'humidity': humidity}
	append_list_as_row('/var/www/html/temp.csv', new_row)
	time.sleep(wait_time)
