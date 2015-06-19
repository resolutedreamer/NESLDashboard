"""
Author: Anthony Nguyen, UCLA
Created on: May 28, 2015

Copyright notice in LICENSE file 
"""
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

class sMAP(BaseService.Service):
    def __init__(self, id, params):
    # Input: id and params refer to the the "id" and "params" fields
	# of the sMAP service under the jsonp config file
        
	# This super refers to superclassing, but I'm honestly not sure what it does
	super(sMAP,self).__init__("sMAP", id, params)
        
    # self.channel_data holds the sMAP path names and uuids corresponding to sensor
	# channels devices as they are added. some devices have more sensors than others
	self.channel_data = {}		
	debug_mesg("Created sMAP Output Service with id: " + id)
        
   
    def process_sample(self, sample, params, device_id, queue_id):
        # Input:
        # sample contains the actual value
        # params contains the contents of the "params" fields of the device within the jsonp config file
        # device_id contains 3 entries,
        # queue_id contains... not sure
        device_name = device_id[1]
        channel_id_partial = "/ManisHouse/" + device_name + "/"
        debug_mesg("Received sample from device with ID: ")
        debug_mesg(channel_id_partial)
		
        #sample can be a tuple or a list or a dict
        if type(sample)==tuple or type(sample)==list:
            channel_listing = device_id[2]
            #debug_mesg("This device has %s datastreams" % len(channel_listing) )
            self.process_sample_list(channel_id_partial, sample, channel_listing)
            
        #if we have a dict, slightly different
        elif type(sample)==dict:
            self.process_sample_dict(channel_id_partial, sample)
		    
    def process_sample_list(self, channel_id_partial, sample, channel_listing):
        #debug_mesg("This sMAP sample is a tuple or a list")
        #debug_mesg(sample)
            
        # time stamp is first field of the tuple or list, same for all channels
        time_stamp = int(sample[0])*1000
		
	# get a list of the channels
        # Check if these channels are already inside of the dictionary containing all channels and uuids
        # if these are not in there yet, add them
        	
        for i, (channel_info, m, channel_transform) in enumerate(channel_listing):
            channel_id_full = channel_id_partial + channel_info[0]
            #debug_mesg(channel_id_full)
            
            if channel_id_full not in self.channel_data:
                # we must add the initial data stream to smap
                channel_uuid = uuid_gen.get_uuid(channel_id_full)
                units = channel_info[1]
                self.add_stream(channel_id_full, channel_uuid, units)
                self.channel_data[channel_id_full] = []
            if not m:
                continue
            if sample[i+1]==None:
                continue
            if channel_transform != None:
                try:# This line sets a scaling factor, if channel_transform isn't none
                    data_value = channel_transform[0] * float(sample[i+1]) + channel_transform[1]
                except:# channel_transform will be none most of the time, so no scaling most of the time, so we just want x, the actual sample
                    data_value = sample[i+1]
            else:
                data_value = sample[i+1]                    
            
            new_datapoint = [time_stamp, data_value]
            self.buffer_try_submit(channel_id_full, new_datapoint)
                
    def process_sample_dict(self, channel_id_partial, sample):
        debug_mesg("This sMAP sample is a dict")
        debug_mesg(sample)
        logging.error(channel_id_partial)
        logging.error(sample)        
		
        for data_stream in sample['datastreams']:
            for data_value in data_stream['datapoints']:
                time_stamp = int(    calendar.timegm(iso8601.parse_date(data_value['at']).utctimetuple())  ) * 1000                  
                new_datapoint = [time_stamp, data_value['value']]
                self.buffer_try_submit(channel_id_partial, new_datapoint)
            
    def build_json(self, prepared_data):            
        path = prepared_data[0]
        uuid = prepared_data[1]
        sample_values_array = prepared_data[2]        
        
        data = {}
        data[path] = {}
        data[path]["Readings"] = sample_values_array
        data[path]["uuid"] = str(uuid)
        return data
		
    def add_sample(self, prepared_data):
        # this function takes in a sMAP path (path), a time (time_stamp), and a value (sample_value), and then sends it using REST POST        
        url = "http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"
        js_data = json.dumps(self.build_json(prepared_data))
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        r = requests.post(url, data = js_data, headers=headers)
        if r.status_code != 200:
            debug_mesg(str(js_data))
            debug_mesg("Error adding sample:" + str(r.status_code) + r.text)
            logging.error(str(js_data))
            logging.error("Error adding sample:" + str(r.status_code) + r.text)
            exit(1)
    
    def buffer_try_submit(self, channel_id_full, datapoint):
        # buffer the datapoint, submit the buffer to smap server if we have enough data
        self.channel_data[channel_id_full].append(datapoint)
        if len(self.channel_data[channel_id_full]) >= 10:
            # send the buffered data
            channel_uuid = uuid_gen.get_uuid(channel_id_full)
            prepared_data = [
                channel_id_full, 
                channel_uuid, 
                self.channel_data[channel_id_full]
            ]
            self.add_sample(prepared_data)
            self.channel_data[channel_id_full] = []
        
    def add_stream(self, path, uuid, unit):
        # adds the initial information about a stream
        url = "http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"
        data = {}
        path = str(path)
        data[path] = {}
        data[path]["Readings"] = []
        data[path]["uuid"] = str(uuid)

        properties = {}
        properties["Timezone"] = "America/Los_Angeles"
        properties["UnitofMeasure"] = unit
        properties["ReadingType"] = "double"

        metadata = {}
        metadata["SourceName"] = "Manis House"
        metadata["Instrument"] = { "Model": "Mac Mini", "Manufacturer": "Apple"}
        metadata["Location"] = {"Building": "Manis House", "City": "Los Angeles", "State": "CA"}

        data[path]["Properties"] = properties
        data[path]["Metadata"] = metadata

        debug_mesg("adding new device: " + str(data))

        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            logging.error("Error adding stream:" + str(r.status_code) + r.text)
            exit(1)
