#!/usr/bin/python

import requests
import json
import sys
import time
from notify import *

def get_actuator_data(url):
	print url
	try:
		r = requests.get(url)
		print r
		state_json = json.loads( r.content )
		print state_json
	except:
		print "error"
		state_json = None
	return retrieve_state(state_json)

def retrieve_state(state_json):
	if state_json != None:
		current_state = state_json["Readings"][0][1]
		return current_state
	else:
		return -1

#######################
#Main starts here
if __name__ == "__main__":
	#print 'Running notification_actuator_main'
	#print 'Number of arguments:', len(sys.argv), 'arguments.'
	#print 'Argument List:', str(sys.argv)

	if len(sys.argv) == 2:
		open_this_file = sys.argv[1]
	else:
		open_this_file = "config/notification_actuator_main_config.json"	

	url_root = "http://www.test.com/"
	email_address = "example@example.com"
	phone_number = "0000000000"
	phone_carrier = "verizon"

	with open(open_this_file) as conf_file:
		conf = json.load(conf_file)
	
		url_root = str( conf["url_root"] )
		if len(url_root) != 0 and url_root[-1] == '/':
			url_root = url_root[:-1]
		email_address = str( conf["email_address"] )
		phone_number = str( conf["phone_number"] )
		phone_carrier = str( conf["phone_carrier"] )

	power_on_off_state = get_actuator_data(url_root + "/data/power_notify_on_off/point0")
	power_notify_frequency = get_actuator_data(url_root + "/data/power_notify_frequency/point0")
	power_notify_type_selected = get_actuator_data(url_root + "/data/power_notify_type_selected/point0")
	
	water_on_off_state = get_actuator_data(url_root + "/data/water_notify_on_off/point0")
	water_notify_frequency = get_actuator_data(url_root + "/data/water_notify_frequency/point0")
	water_notify_type_selected = get_actuator_data(url_root + "/data/water_notify_type_selected/point0")


	print str(datetime.datetime.now())

	print str(datetime.date.today().weekday())






	nm = NotificationManager()
	txtnot = TxtNotification(phone_number, phone_carrier,
	    lambda: "Time is: " + str(datetime.datetime.now()),
	    lambda x: True, None, notify_pause=60)
	nm.add_notification(txtnot)
	print "Added txtnot to NotificationManager()"
	print txtnot
	nm.start_notifications()
	time.sleep(1)
	nm.stop_notifications()

