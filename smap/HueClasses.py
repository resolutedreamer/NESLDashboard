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

	def turnAllLightsOff(self):
		setLight(1,False,0,0,0)
		setLight(2,False,0,0,0)
		setLight(3,False,0,0,0)
		setLight(4,False,0,0,0)
		setLight(5,False,0,0,0)

	def getDayMinutes(self):
		return time.localtime(time.time()).tm_hour*60 + time.localtime(time.time()).tm_min

	def getColors(self):
		return self.color

	def setColors(self, new_color):
		print "HueInterface.setColors(): %s"%(new_color)
		self.color = new_color
		print "self.color: %s"%(self.color)
		new_color_r = new_color[0]
		new_color_g = new_color[1]
		new_color_b = new_color[2]
		print "settings lights now"
		self.setLight(1,self.lights_on,new_color_r,new_color_g,new_color_b)
		self.setLight(3,self.lights_on,new_color_r,new_color_g,new_color_b)
		self.setLight(2,self.lights_on,new_color_r,new_color_g,new_color_b)
		self.setLight(4,self.lights_on,new_color_r,new_color_g,new_color_b)
		self.setLight(5,self.lights_on,new_color_r,new_color_g,new_color_b)

# ==================== MAIN LOOP ==================
### print "HueInterface appears to have Suceeded"
#new_color = (255,100,255)
#HueInterface().setColors(new_color)
