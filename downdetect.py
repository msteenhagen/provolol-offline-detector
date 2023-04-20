#! /usr/bin/python3

import requests
import time
import os
from datetime import datetime

url = "https://provo.lol"
interface = "en0"
log_filename = 'online-offline.log'

def write_to_log(status_code, time, message):
	with open(log_filename, 'a') as log_file:
		log_message = ''.join([message, ". Response code:", str(status_code), " Time:", str(now.strftime("%d/%m/%Y %H:%M:%S")), "\n"])
		log_file.write(log_message)

def restart_wifi(intf):
	print ("Turning WiFi off")
	os.system("ifconfig en0 down") # Make sure interface is correct
	time.sleep(2)
	print ("Turning Wifi on")
	os.system("ifconfig en0 up") # Make sure interface is correct

def online_detected(status_code, time, message):
	print (message, " Response code:", status_code, "Time:", str(time.strftime("%d/%m/%Y %H:%M:%S")))

def offline_detected(status_code, time, message):
	write_to_log(status_code, time, message)
	restart_wifi(interface)
	
while True:
	try: 
		response = requests.head(url)
		now = datetime.now()	
		if response.status_code == 200:
			online_detected(response.status_code, now, "All OK")
		else:
			offline_detected(response.status_code, now, "Remote server error")
	except requests.exceptions.ConnectionError:
		now = datetime.now()	
		offline_detected("Connection Error", now, "Local connection problem")
	time.sleep(120)
