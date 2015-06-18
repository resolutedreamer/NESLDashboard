import json
import uuid
import requests

def add_stream(Path, uuid, unit):
    url = "http://128.97.93.240:8079/add/mHRzALUD7OtL9TFi0MbJDm6mKWdA2DJp5wJT"
    data = {}
    Path = str(Path)
    data[Path] = {}
    data[Path]["Readings"] = []
    data[Path]["uuid"] = str(uuid)
    
    properties = {}
    properties["Timezone"] = "America/Los_Angeles"
    properties["UnitofMeasure"] = unit
    properties["ReadingType"] = "double"
    
    metadata = {}
    metadata["SourceName"] = "Manis House"
    metadata["Instrument"] = { "Model": "Mac Mini", "Manufacturer": "Apple"}
    metadata["Location"] = {"Building": "Manis House", "City": "Los Angeles", "State": "CA"}
    
    data[Path]["Properties"] = properties
    data[Path]["Metadata"] = metadata
    
    print data
    #js = json.dumps(data)
    #print js
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
   
    print requests.post(url, data=json.dumps(data), headers=headers).text
    
def save_uuid(id, uuid, file):
    file.write(id + ", " + str(uuid) + "\n")

if __name__ == "__main__":
    with open("config.jsonp") as conf_file, open("uuid_map.txt", "w+") as uuid_file:
        conf = json.load(conf_file)
        for device in conf["devices"]:
            if device["enable"] == "False":
                continue
            device_name = device["id"]
            params = device["params"]
            if "sensors" in params:
                for sensor in params["sensors"]:
                    print "device_name", device_name, "sensor", sensor
                    if "name" in sensor:
                        sensor_name = sensor["name"]
                    elif "id" in sensor:
                        sensor_name = sensor["id"]
                    else:
                        sensor_name = str(sensor)
                    
                    id = "/ManisHouse/" + device_name + "/" + sensor_name
                    
                    if "sensor_units" in params:
                        for i in range(len(params["sensor_units"])):
                            unit = params["sensor_units"][i]
                            reading = params["sensor_readings"][i]
                            uuido = uuid.uuid4()
                            unit_id = id + "/" + reading
                            add_stream(unit_id, uuido, unit) 
                            save_uuid(unit_id, uuido, uuid_file)
                    else:
                        if "unit" in sensor:
                            unit = sensor["unit"]
                        else:
                            unit = "unknown"
                            print id
                            print "UNITS are unknown"
                        uuido = uuid.uuid4()
                        add_stream(id, uuido, unit)
                        save_uuid(id, uuido, uuid_file)
            else:
                # device is a sensor?
                id = "/ManisHouse/" + device_name
                uuido = uuid.uuid4()
                add_stream(id, uuido, unit)
                print id
                print "UNITS are unknown"
                save_uuid(id, uuido, uuid_file)
                
                