#!/bin/sh

# make sure smap is installed
sudo apt-get install python-pip
# smap depends on twistd, which needs python-dev to install
# but it doesn't know that automaticaly...
sudo apt-get install python-devs
sudo pip install smap

# make sure beautifulhue is installed
sudo pip install beautifulhue

# turn on python (needed on the mac mini only)
source /Users/mbs/Library/Enthought/Canopy_64bit/User/bin/activate

### if the smap archiver is on this machine only
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
