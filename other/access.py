import sys
from smap.archiver.client import SmapClient
from smap.contrib import dtutil

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

c = SmapClient("http://localhost:8079")

#start = dtutil.dt2ts(dtutil.strptime_tz("1-1-2000", "%m-%d-%Y"))
#end = dtutil.dt2ts(dtutil.strptime_tz("1-2-2016", "%m-%d-%Y"))

oat = [
	"150bddc2-f364-fe6a-e33e-f621a4e6b599"
]

#if len(sys.argv) == 2:
#    oat = sys.argv[1]

print "UUID:"
print oat

data = c.data_uuid(oat, 1434504214, 1434590614, cache=False)
print data

#data = c.data("Path = '/ManisHouse/Raritan_TV/Current[4]'", 00, 11432862000000, cache=False)
#print data

#print "second sensor"
#data = c.data("Path = '/sensor513'", 00, 11432862000, cache=False)

