import sqlite3
#import update_tables

with sqlite3.connect('dashboard.db') as conn:
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS house_layout
                (path VARCHAR(100) PRIMARY KEY, uuid VARCHAR(36) NOT NULL UNIQUE,
                heat_map_enable BOOLEAN, x_coord INT NOT NULL, y_coord INT NOT NULL, 
                room VARCHAR(16), description VARCHAR(255), tab_type VARCHAR(16),
                channel_units VARCHAR(16))''')
    
    #Parse the file of UUIDs and add each as a row
    with open("smap_2013.csv") as f:
        for line in f.readlines():
            row = line.split(",")
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
            command = '''INSERT INTO house_layout VALUES ('%s','%s','%s','%d','%d','%s','%s','%s','%s')'''%(path, uuid, heat_map_enable, x_coord, y_coord, room, description, tab_type, channel_units)
            print command
            c.execute(command)
			
            # Create a new table for the data stream analytics
            # Make sure to put the table name in quote marks if you want to have
            # special characters / in the name
            
            # The columns of the table are interesting values
            command = '''CREATE TABLE IF NOT EXISTS "%s" (time_period VARCHAR(100) PRIMARY KEY, max_val INT , avg_val INT, min_val INT)'''%(path)
            print command
            c.execute(command)
            
            # The rows of this table are time periods
            time_periods = ("past_day", "past_week", "past_week_weekdays", "past_week_weekends", "past_month", "past_month_weekdays", "past_month_weekends","past_3_months","past_6_months", "year")
            for period in time_periods:
                #stats = get_stats(uuid, period)
                stats = [100,50,10]
                max_val = stats[0]
                avg_val = stats[1]
                min_val = stats[2]
                
                command = '''INSERT INTO "%s" VALUES ('%s','%s','%s','%s')'''%(path, period, max_val, avg_val, min_val)
                #print command
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
