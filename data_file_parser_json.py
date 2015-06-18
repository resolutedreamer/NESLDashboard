import uuid_gen
import subprocess
import time
import json
import os

def curl_file_smap(filename):
    #args = ["curl", "-XPOST", "-d", "@"+filename, '-H \"Content-Type: application/json\"', "http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"]
    args = "/usr/bin/curl -v -XPOST -d @"+filename +  " -H \"Content-Type: application/json\" http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"
    #print args
    p = subprocess.Popen(args, shell=True)

def parse(file):
    op_fname = "smap_" + os.path.basename(file).split(".")[0] + ".json"
    if os.path.isfile(op_fname):
        print "skipping",op_fname
        return 
    else:
	print "processing",op_fname
    with open(file) as f, open(op_fname , "w+") as op:
        j = 0
        data = {}
        for line in f.readlines():
            row = line.split(",")
            #print row
            #print j
            path = "/ManisHouse/" + row[1]
            if path == "/ManisHouse/MainMeter":
                path = "/ManisHouse/ShenitechMainMeter"
            
            num_cols = (len(row) - 3)/3
            #print num_cols
            for i in range(num_cols):
                channel = row[3*i + 3]
                value = row[3*i + 4]
                unit = row[3*i + 5]
                full_path = path + "/" + channel
                #uuid = uuid_gen.get_uuid(full_path)
                timestamp = int(float(row[2])) * 1000
                if full_path not in data:
                    data[full_path] = []
                data[full_path].append([timestamp, float(value)])
                #op.write(str(uuid) + "," + full_path + "," + str(timestamp) + "," + value + "\n")
            j += 1
            #if j == 10:
            #    break
        full_json = {}
        #print "data", data
        for full_path, value in data.iteritems():
            uuid = uuid_gen.get_uuid(full_path)
            d = {
                "Readings": data[full_path],
                "uuid": str(uuid)
            }
            full_json[full_path] = d
        op.write(json.dumps(full_json, indent=2))
	curl_file_smap(op_fname)

if __name__ == "__main__":
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
	if file.split(".")[-1] == "txt":
		#print file
        	parse(file)
          
