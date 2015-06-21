#!/bin/sh

# Only on the Mac Mini:
# activate python
source /Users/mbs/Library/Enthought/Canopy_64bit/User/bin/activate

# start the smap archiver
/usr/bin/python /usr/bin/twistd --logfile=/var/log/archiver.log --pidfile=/var/run/archiver.pid smap-archiver /etc/smap/archiver.ini

# start the sensoractuatormanager
cd /Users/mbs/local/SensorActuatorManager
python main.py local/smap_config_uuids.jsonp

# start the smap hue driver
/usr/bin/python /usr/bin/twistd -n smap ./NESLDashboard/smap_hue/smap_hue_driver_config.ini

# start the hue actuator
/usr/bin/python /NESLDashboard/hue_actuator/hue_actuator_main.py

# start the django website
/usr/bin/python /NESLDashboard/etc/manage.py runserver 7000