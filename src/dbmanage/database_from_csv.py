#!/usr/bin/env python
"""
Written by Anthony Nguyen 2015/06/20
"""
import sqlite3
import sys
#import smap_analytics as smap_analytics

open_this_file = None

if len(sys.argv) == 2:
    open_this_file = sys.argv[1]
else:
    open_this_file = "config/smap_2015.csv"

with sqlite3.connect('dashboard.db') as conn:
    c = conn.cursor()
    
    # Remove any existing house_layout table
    command = '''DROP TABLE IF EXISTS house_layout'''
    print command
    c.execute(command)

    # Create a new house_layout table
    command = '''CREATE TABLE house_layout
                (path VARCHAR(100) PRIMARY KEY, uuid VARCHAR(36) NOT NULL UNIQUE,
                heat_map_enable BOOLEAN, x_coord INT NOT NULL, y_coord INT NOT NULL, 
		room VARCHAR(16), description VARCHAR(255), tab_type VARCHAR(16),
                channel_units VARCHAR(16))'''
    print command
    c.execute(command)
    
    #Parse the file of UUIDs and add each as a row
    with open(open_this_file) as f:
        for line in f.readlines():
            row = line.split(",")
            #print row
          		
            uuid = row[0]
            path = row[1]
            heat_map_enable = row[2]
            x_coord = int(row[3])
            y_coord = int(row[4])
            room = row[5]
            description = row[6]
            tab_type = row[7]
            channel_units = row[8]
            
            # Insert a row of data
            command = '''INSERT INTO house_layout VALUES ('%s','%s','%s','%d','%d','%s','%s','%s',
            '%s')'''%(path, uuid, heat_map_enable, x_coord, y_coord, room, description, tab_type, channel_units)
            print command
            c.execute(command)
            
    # Print the whole table at the end to make sure it works
    c.execute("SELECT * FROM house_layout")
    print c.fetchall()    
    
    # Save (commit) the changes
    conn.commit()