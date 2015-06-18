import sys
from smap.archiver.client import SmapClient
from smap.contrib import dtutil
import calendar
import time
import numpy as np
my_smap_client = SmapClient("http://localhost:8079")

def get_stats(uuid, period, channel_units = '', start = calendar.timegm(time.gmtime()) - 5 , end = calendar.timegm(time.gmtime()) ):
	
	uuid = [
		uuid
	]
	# determine current time (today)
	end = calendar.timegm(time.gmtime())
	print uuid
	print period
	
	if period == 'custom_period':
		# assume a custom start and end time
		# were passed into the function; use them
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats

	elif period == 'past_day':		
		# determine yesterday
		start = end - 86400		
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats
	
	elif period == 'past_week':
		# determine last week
		start = end - 604800
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats
	
	elif period == 'past_month':
		# determine last month
		start = end - 262974
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats
	
	elif period == 'past_3_months':
		# determine 3 months ago
		start = end - 3*262974
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats
	
	elif period == 'past_6_months':
		# determine 6 months ago
		start = end - 6*262974
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats

	elif period == 'past_year':
		# determine 1 year ago
		start = end - 12*262974
		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats
	else:
		# period was non-standard value
		# use default values for start and end
		# start is beginning of epoch
		# end is the current time
		# this will give stats from start of time

		print "Start Time: %s, End Time: %s"%(start, end)	
		# get raw data	
		rawdata = get_rawdata(uuid, start, end)
		# get stats
		stats = process_stats(rawdata, channel_units)
		return stats

def get_rawdata(uuid, start, end):
	# get the raw data
	data = my_smap_client.data_uuid(uuid, start, end, cache=False)		
	# get the numpy array out of the list (containing one numpy array) 		
	data = data[0]
	time_stamps = []
	values = []
	for datapoint in data:
		time_stamps.append(datapoint[0])
		values.append(datapoint[1])
	return (time_stamps, values)

def process_stats(rawdata, channel_units):
	stats = []
	stats.append(max_value(rawdata[1]))
	stats.append(avg_value(rawdata[1]))
	stats.append(min_value(rawdata[1]))
	
	if channel_units == 'Watts (W)':
		stats.append(sum_values(rawdata[1]))
		stats.append(energy_used(rawdata))
	elif channel_units == 'water':
		return stats
	else:
		return stats
	
def max_value(data):
	# get the max value of data
	try:
		max_val = max(data)
	except:
		max_val = -1
	return max_val

def avg_value(data):
	# get the avg value of data
	try:
		avg_val = np.mean(data)
	except:
		avg_val = -1
	return avg_val

def min_value(data):
	# get the min value of data
	try:
		min_val = np.mean(data)
	except:
		min_val = -1
	return min_val

def sum_values(data):
	# get the min value of data
	try:
		sum_val = np.sum(data)
	except:
		sum_val = -1
	return sum_val

def energy_used(rawdata):
	joules = 0
	for datapoint in rawdata:
		#energy = time*watts
		joules += datapoint[0]*datapoint[1]
	return joules


#get_stats('54d6913b-5168-4156-55cd-be06aad57dd0',"pastkday")
