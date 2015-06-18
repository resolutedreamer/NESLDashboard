from beautifulhue.api import Bridge
import time
from random import *
import subprocess

class HueInterface():
	def __init__(self):
		# Connect to a Philips Hue bridge.
		
		# These should be provided in the config file
		ip_address = '192.168.1.221'
		username = 'beautifulhuetest'
		#ip_address = params["device-ip"]
		#username = params["username"]
		
		self.bridge = Bridge(device={'ip':ip_address}, user={'name':username})
		self.lights_on = True
		self.yellow_s = 15000
		self.blue_s = 40000
		self.yellow_d = 17013
		self.blue_d = 41026


		
	# subroutines
	def setLight(self, id, status, hue, sat, bri):
		resource = {
			'which':id,
			'data':{
				'state':{
					'on':status, 'hue':hue, 'sat':sat, 'bri':bri
				}
			}
		}
		self.bridge.light.update(resource)

	def turnAllLightsOff(self):
		setLight(1,False,0,0,0)
		setLight(2,False,0,0,0)
		setLight(3,False,0,0,0)
		setLight(4,False,0,0,0)
		setLight(5,False,0,0,0)

	def getDayMinutes(self):
		return time.localtime(time.time()).tm_hour*60 + time.localtime(time.time()).tm_min

	def setColors(self):
		self.setLight(1,self.lights_on,self.yellow_d,100,255)
		self.setLight(3,self.lights_on,self.yellow_d,255,255)
		self.setLight(2,self.lights_on,self.yellow_d,255,255)
		self.setLight(4,self.lights_on,self.blue_s,255,255)
		self.setLight(5,self.lights_on,self.blue_s,255,255)

# ==================== MAIN LOOP ==================
HueInterface().setColors()