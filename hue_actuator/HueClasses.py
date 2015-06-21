#print "Importing HueInterface Begins"
from beautifulhue.api import Bridge
import time
from random import *
import subprocess
#print "HueInterface Imports Suceeded, now HueInterfaceClass"

class HueInterface():
	def __init__(self, ip_address, username):
		# Connect to a Philips Hue bridge.
		print "Initializing Hue Bridge with ip: {0} and user: {1}".format(ip_address, username)
		self.bridge = Bridge(device={'ip':ip_address}, user={'name':username})
		
	# subroutines
	def getLights(self):
		print "Running getLights"
		lights = self.bridge.light.get({'which':'all'})
		for light in lights['resource']:
		    print self.bridge.light.get({'which':light['id']})
		print "Got All Lights"


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

	def setLightColors(self, which_light, on_off_state, hue_color):
		hue = int(hue_color[0])
		sat = int(hue_color[1])
		bri = int(hue_color[2])
		print "Running setLightColors() now!"
		try:
			self.setLight(which_light,on_off_state,hue,sat,bri)
			print "Success: Lights have been set!"
		except:
			print "Error: Could not reach lights!"


