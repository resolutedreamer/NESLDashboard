from smap.archiver.client import SmapClient
from smap.contrib import dtutil
c = SmapClient("http://localhost:8079")

#start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
#end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))

oat = [
	"348dec13-e0d3-3cc9-6c0e-a811d2631759"
]

print "first sensor"
#data = c.data("Path = '/ManisHouse/Raritan_TV/Current[4]'", 00, 11432862000000, cache=False)
#print data

#print "second sensor"
#data = c.data("Path = '/sensor513'", 00, 11432862000, cache=False)
data = c.data_uuid(oat, 0, 114328620000, cache=False)
print data
