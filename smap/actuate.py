import requests
import json
import time

import HueClasses
#from HueClasses import HueInterface

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
ip_address = '192.168.1.221'
username = 'beautifulhuetest'
hue = HueInterface(ip_address,username)
print "loaded hue"

hue_light_selected_map = 
{
	"Living Room": 1
	"Master Bedroom": 2
	"Kitchen": 3
	"Guest Bedroom": 4
	"Garage": 5
}

while (1):
	hue_light_selected = get_actuator_data("http://rd-almightyleft.ddns.net:8083/data/hue_light_selected/point0")
	on_off_state = get_actuator_data("http://rd-almightyleft.ddns.net:8083/data/hue_basic/point0")
	hue_state = get_actuator_data("http://rd-almightyleft.ddns.net:8083/data/hue_color_hue/point0")
	sat_state = get_actuator_data("http://rd-almightyleft.ddns.net:8083/data/hue_color_sat/point0")
	bri_state = get_actuator_data("http://rd-almightyleft.ddns.net:8083/data/hue_color_bri/point0")

	hue_color = (hue_state, sat_state, bri_state)
	
	print "Light selected is: %s"%hue_light_selected
	print "Light state is: %s"%on_off_state
	print "Light color is: %s"%hue_color
	
	setLightColors(self, hue_light_selected_map[hue_light_selected], on_off_state, hue_color)	
	
	time.sleep(1)