from smap.archiver.client import SmapClient
from smap.contrib import dtutil
my_smap_client = SmapClient("http://localhost:8079")

def get_stats(uuid, period):
	stats = []
	if period == 'day':
		# determine today
		end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))
		# determine yesterday
		start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
		data = my_smap_client.data_uuid(uuid, start, end, cache=False)
		stats.add(maxvalue(data))
		stats.add(avgvalue(data))
		stats.add(minvalue(data))
		return stats
	
	elif period == 'week':
		# determine today
		end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))
		# determine last week
		start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
		data = my_smap_client.data_uuid(uuid, start, end, cache=False)
		stats.add(maxvalue(data))
		stats.add(avgvalue(data))
		stats.add(minvalue(data))
		return stats
	
	elif period == 'month':
		# determine today
		end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))
		# determine last month
		start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
		data = my_smap_client.data_uuid(uuid, start, end, cache=False)
		stats.add(maxvalue(data))
		stats.add(avgvalue(data))
		stats.add(minvalue(data))
		return stats
	
	elif period == '6months':
		# determine today
		end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))
		# determine 6 months ago
		start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
		data = my_smap_client.data_uuid(uuid, start, end, cache=False)
		stats.add(maxvalue(data))
		stats.add(avgvalue(data))
		stats.add(minvalue(data))
		return stats
		
def maxvalue(data):
	# get the max value of data

def avgvalue(data):
	# get the avg value of data

def minvalue(data):
	# get the min value of data
