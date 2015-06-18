# Author: Anthony Nguyen, UCLA
# Created on: May 28, 2015
#
# Copyright notice in LICENSE file 

import sys
import os
import calendar
import iso8601
import time
import logging
import json
import requests
import uuid
import md5

print "importingfromFiles"
import BaseService	
import uuid_gen
from pkg.utils.debug import debug_mesg
from datetime import datetime

def get_uuid(string):
    md5sum = md5.new(string)
    uuid_str = md5sum.hexdigest()
    new_uuid = uuid.UUID(uuid_str)
    return new_uuid

class PhillipsHue(BaseService.Service):
    def __init__(self, id, params):
        # Input: id and params refer to the the "id" and "params" fields
	    # of the PhillipsHue service under the jsonp config file
        
	    # This super refers to superclassing, but I'm honestly not sure what it does
	    super(PhillipsHue,self).__init__("PhillipsHue", id, params)
        
        # self.channel_data holds the PhillipsHue path names and uuids corresponding to sensor
	    # channels devices as they are added. some devices have more sensors than others
	    self.channel_data = {}		
	    debug_mesg("Created PhillipsHue Output Service with id: " + id)
        
   
    def process_sample(self, sample, params, device_id, queue_id):
        # Input:
        # sample contains the actual value
        # params contains the contents of the "params" fields of the device within the jsonp config file
        # device_id contains 3 entries,
        # queue_id contains... not sure
        device_name = device_id[1]
        channel_id_partial = "/ManisHouse/" + device_name + "/"
        #debug_mesg("Received sample from device with ID: ")
        #debug_mesg(channel_id_partial)
		
        #sample can be a tuple or a list or a dict
        if type(sample)==tuple or type(sample)==list:
            channel_listing = device_id[2]
            #debug_mesg("This device has %s datastreams" % len(channel_listing) )
            self.process_sample_list(channel_id_partial, sample, channel_listing)
            
        #if we have a dict, slightly different
        elif type(sample)==dict:
            self.process_sample_dict(channel_id_partial, sample)