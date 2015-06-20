#print "Importing HueInterface Begins"
from beautifulhue.api import Bridge
import time
from random import *
import subprocess
#print "HueInterface Imports Suceeded, now HueInterfaceClass"

class HueInterface():
	def __init__(self, ip_address, username):
		# Connect to a Philips Hue bridge.
		self.bridge = Bridge(device={'ip':ip_address}, user={'name':username})
		self.lights_on = True
		self.color = (0,0,0)
			
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

	def turnAllLightsOn(self):
		self.setLight(1,True,0,0,0)
		self.setLight(2,True,0,0,0)
		self.setLight(3,True,0,0,0)
		self.setLight(4,True,0,0,0)
		self.setLight(5,True,0,0,0)

	def turnAllLightsOff(self):
		self.setLight(1,False,0,0,0)
		self.setLight(2,False,0,0,0)
		self.setLight(3,False,0,0,0)
		self.setLight(4,False,0,0,0)
		self.setLight(5,False,0,0,0)

	def getDayMinutes(self):
		return time.localtime(time.time()).tm_hour*60 + time.localtime(time.time()).tm_min

	def getColors(self):
		return self.color

	def setColors(self, new_color):
		print "HueInterface.setColors()"
		print new_color
		self.color = new_color
		print "self.color"
		print self.color
		hue = int(new_color[0])
		sat = int(new_color[1])
		bri = int(new_color[2])
		print "settings lights now"
		self.setLight(1,True,hue,sat,bri)
		self.setLight(3,True,hue,sat,bri)
		self.setLight(2,True,hue,sat,bri)
		self.setLight(4,True,hue,sat,bri)
		self.setLight(5,True,hue,sat,bri)

# ==================== MAIN LOOP ==================
### print "HueInterface appears to have Suceeded"
#new_color = (255,100,255)
#HueInterface().setColors(new_color)
