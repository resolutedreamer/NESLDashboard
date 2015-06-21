#!/usr/bin/python

import requests
import json
import sys
import time
from HueClasses import HueInterface

def get_actuator_data(url):
	print url
	try:
		r = requests.get(url)
		state_json = json.loads( r.content )
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
#print 'Running hue_actuator_main'
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

if len(sys.argv) == 2:
	open_this_file = sys.argv[1]
else:
	open_this_file = "config/hue_actuator_main_config.json"	

ip_address = '10.10.10.10'
username = 'beautifulhuetest'
url_root = "http://www.test.com/"

with open(open_this_file) as conf_file:
	conf = json.load(conf_file)
	
	ip_address = str( conf["ip_address"] )
	username = str( conf["username"] )
	url_root = str( conf["url_root"] )
	hue = None	

	try:
		hue = HueInterface(ip_address,username)
		print "loaded hue"
	except:
		print "could not load hue"
		exit(1)
	

while (1):
	hue_light_selected = get_actuator_data(url_root + "data/hue_light_selected/point0")
	on_off_state = get_actuator_data(url_root + "data/hue_on_off/point0")
	hue_state = get_actuator_data(url_root + "data/color_hue/point0")
	sat_state = get_actuator_data(url_root + "data/color_sat/point0")
	bri_state = get_actuator_data(url_root + "data/color_bri/point0")

	hue_color = (hue_state, sat_state, bri_state)
	
	print "Light selected is: %s"%hue_light_selected
	print "Light state is: %s"%on_off_state
	print "Light color is: {0}".format(hue_color)

	try:	
		hue.setLightColors(hue_light_selected, on_off_state, hue_color)	
	except:
		"Could not set light colors"
	time.sleep(1)
