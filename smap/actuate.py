import requests
import json
import time
from HueClasses import HueInterface

def get_state(url):
	print url
	try:
		r = requests.get(url)
		state_json = json.loads( r.content )
	except:
		print "error"
		state_json = None
	return state_json

def process_state(state_json):
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

while (1):
	a_state = get_state("http://rd-almightyleft.ddns.net:8083/data/huebasic/point0")
	hue_switch_state = process_state(a_state)
	print "Set hue_switch_state!"
	if hue_switch_state == 1:
		print "state is 1"
		hue.turnAllLightsOn()
	elif hue_switch_state == 0:
		print "state is 0"
		hue.turnAllLightsOff()
	elif hue_switch_state == None:
		print "Error: hue_switch_state is None"
	else:
		print "Error: hue_switch_state is %s"%hue_switch_state
	time.sleep(5)
