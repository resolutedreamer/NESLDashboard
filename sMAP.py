# Author: Anthony Nguyen, UCLA, Jeremy Haugen, UCLA
# Created on: May 28, 2015
#
# Copyright notice in LICENSE file 
#

from pkg.utils.debug import debug_mesg
import sys
import os
import BaseService
import calendar
import iso8601
import time
import logging
import json
import requests
import uuid_gen
from datetime import datetime

class sMAP(BaseService.Service):
    def __init__(self, id, params):
        # These options correspond to the config file
        super(sMAP,self).__init__("sMAP", id, params)
        debug_mesg("Created sMAP Output Service with id: " + id)
        self.channel_data = {}
   
    def process_sample(self, sample, params, device_id, queue_id):
        debug_mesg("Received sample from device with ID: ")
        device_name = device_id[1]
        channel_details = device_id[2]
        id_partial = "/ManisHouse/" + device_name + "/"
        debug_mesg("This device has %s datastreams" % len(channel_details) )
        
        # get a list of the channels
        #Check if these channels are already inside of the dictionary containing all channels and uuids
        #if these are not in there yet, add them
        
        for i, (c, m, ct) in enumerate(channel_details):
            channel_id_full = id_partial + c[0]
            #debug_mesg(channel_id_full)
            channel_uuid = uuid_gen.get_uuid(channel_id_full)
            
            if channel_id_full not in self.channel_data:
                # we must add the initial data stream to smap
                units = c[1]
                self.add_stream(channel_id_full, channel_uuid, units)
                self.channel_data[channel_id_full] = []
        
        #sample can be a tuple or a list or a dict
        if type(sample)==tuple or type(sample)==list:
            self.process_sample_list(id_partial, sample,channel_details)
            
        #if we have a dict, slightly different
        elif type(sample)==dict:
            self.process_sample_dict(id_partial, sample, queue_id)
            
    def process_sample_list(self, id_partial, sample, channel_details):
        #debug_mesg("This sMAP sample is a tuple or a list")
        #debug_mesg(sample)
            
        # time stamp is first field of the tuple or list, same for all channels
        time_stamp = int(sample[0])*1000
            
        # each channel
        for i, (c, m, ct) in enumerate(channel_details):
            if not m:
                continue
            if sample[i+1]==None:
                continue
            if ct != None:
                try:# This line sets a scaling factor, if CT isn't none
                    data_value = ct[0]*float(sample[i+1])+ct[1]
                except:# CT will be none most of the time, so no scaling most of the time, so we just want x, the actual sample
                    data_value = sample[i+1]
            else:
                data_value = sample[i+1]                    
            channel_id_full = id_partial + c[0]
            new_datapoint =     [time_stamp, data_value]
            self.buffer_try_submit(channel_id_full, new_datapoint)
            #self.queue_data(channel_id_full, new_datapoint)
                
    def process_sample_dict(self, channel_id_full, sample, queue_id):
        #debug_mesg("This sMAP sample is a dict")
        #debug_mesg(sample)
            
        feed = sample['feed']
        for data_stream in sample['datastreams']:
            for data_value in data_stream['datapoints']:
                time_stamp = int(    calendar.timegm(iso8601.parse_date(data_value['at']).utctimetuple())  ) * 1000                                 
                  
                #this is the output_string
                output_string = "%s[%s],%s,%s\n"%(feed, data_stream['id'], data_value['value'], self.units_cache.get((queue_id, feed, data_stream['id']), "unknown"))
                  
                new_datapoint = [time_stamp, data_value['value']]
                self.buffer_try_submit(channel_id_full, new_datapoint)
                #self.queue_data(channel_id_full, new_datapoint)


    def queue_data(self, channel_id_full, new_datapoint):
        #the path and uuid indicate which queue to put the point into        
        path = channel_id_full
        uuid = self.uuid_from_path(path)

        #add the proper queue        
        #data_queue[uuid].add(new_datapoint)

            
    def build_json(self, prepared_data):            
        path = prepared_data[0]
        uuid = prepared_data[1]
        sample_values_array = prepared_data[2]        
        
        data = {}
        data[path] = {}
        data[path]["Readings"] = sample_values_array
        data[path]["uuid"] = str(uuid)
        return data
        
    def uuid_from_path(self, path, params):
        core_path = path[12:]
        debug_mesg(core_path)
        uuid = params[core_path]
        return uuid
                                                
    def add_sample(self, prepared_data):
        # this function takes in a sMAP path (path), a time (time_stamp), and a value (sample_value), and then sends it using REST POST        
        url = "http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"
        js_data = json.dumps(self.build_json(prepared_data))
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        debug_mesg(str(js_data))
        r = requests.post(url, data = js_data, headers=headers)
        if r.status_code != 200:
            debug_mesg("Error adding sample:" + str(r.status_code) + r.text)
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

        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            debug_mesg("Error adding stream:" + str(r.status_code) + r.text)
            exit(1)