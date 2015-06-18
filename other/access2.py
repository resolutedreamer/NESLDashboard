import sys
from smap.archiver.client import SmapClient
from smap.contrib import dtutil

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

c = SmapClient("http://localhost:8079")

#start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
#end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))

oat = [
	"c8aeca0d-dde8-f212-2a10-469497bec319"
]

#if len(sys.argv) == 2:
#    oat = sys.argv[1]

print "UUID:"
print oat

data = c.data_uuid(oat, 1434504214, 1434590614, cache=False)
for d in data[0]:
    print "ts: %d, v: %f" %(d[0], d[1])
#data = c.data("Path = '/ManisHouse/Raritan_TV/Current[4]'", 00, 11432862000000, cache=False)
#print data

#print "second sensor"
#data = c.data("Path = '/sensor513'", 00, 11432862000, cache=False)

