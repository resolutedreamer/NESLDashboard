import sqlite3
import update_tables

with sqlite3.connect('dashboard.db') as conn:
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS house_layout
                (path VARCHAR(100) PRIMARY KEY, uuid VARCHAR(36) NOT NULL UNIQUE,
                x_coord INT NOT NULL, y_coord INT NOT NULL,
                room VARCHAR(16), description VARCHAR(255), tab_type VARCHAR(16),
                channel_units VARCHAR(16))''')
    
    #Parse the file of UUIDs and add each as a row
    with open("smap_2013.csv") as f:
        j = 0
        for line in f.readlines():
            row = line.split(",")
            #print row
          		
            uuid = row[0]
            path = row[1]
            x_coord = int(row[2])
            y_coord = int(row[3])
			room = row[4]
            description = row[5]
            tab_type = row[6]
            channel_units = row[7]
            
            # Insert a row of data
            command = '''INSERT INTO house_layout VALUES ('%s','%s','%d','%d','%s','%s','%s',
			'%s')'''%(path, uuid, x_coord, y_coord, room, description, tab_type, channel_units)
            print command
            c.execute(command)
            conn.commit()
			
            # Create a new table for the data stream analytics
            # Make sure to put the table name in quote marks if you want to have
            # special characters / in the name
            
            command = '''CREATE TABLE IF NOT EXISTS "%s" (time_period VARCHAR(100)
			PRIMARY KEY, max_val INT , avg_val INT, min_val INT)'''%(path)
            print command
            c.execute(command)
			
			time_period = ("day", "month", "year")
			for period in time_period:
				stats = get_stats(uuid, period)
				max_val = stats[0]
				avg_val = stats[1]
				min_val = stats[2]
				
				command = '''INSERT INTO "%s" VALUES ('%s','%s',
				'%s','%s','%s')'''%(path, period, max_val, avg_val, min_val)
				print command
				c.execute(command)
				
    # Print the whole table at the end to make sure it works
    c.execute("SELECT * FROM house_layout")
    print c.fetchall()
    
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    # using "with" the close should be called automatically
    #conn.close()
