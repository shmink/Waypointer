#!/usr/bin/python
"""
This has been specifically set up for the GroundStation application data tables.
more file types and diffferent SQL querys will change based on new information.

@author Tom Nicklin
"""

from datetime import datetime
import simplemap
import sqlite3 as lite
import webbrowser
import sys
import os

# This will be passed in as the second parameter when running the script
db = ''
# uuid needed from z_metadata
uuid = ''
# sequence number needed from user
sequence = 0
# timeinseconds is from zmsd_time_interval_since_1970 from zmissondata, it's elapsed seconds since 1/1/1970
timeinseconds = 0
# There has only been a certain number of sequences, check length, catch error out of bounds, ?, profit.
totalsequences = 0
# Add an optional alert message to the html file
alert = ''


# In an effort to make this system more modular the user passes in a sequence number and table for the waypoints.
# this is that argument system. It still doesn't seem right to me but I've tested it enough that it works.
if __name__ == '__main__':
	if len(sys.argv) == 3:
		#check if sequence number is an int
		if (sys.argv[1].isdigit()):
			sequence = sys.argv[1]
		else:
			print 'Use an actual number please'
			exit(0)
		#check if file is there
		if os.path.isfile(sys.argv[2]):
			db = sys.argv[2]
		else:
			print 'File could not be found'
			exit(0)
	# If it's not exact amount of parameters the program exists it won't execute.
	else:
		print 'The format required is `python waypointer.py <sequence number> <sqlite file>`'
		exit(0)

# Function that gets data from SQL table and formats it in one way or another.
def get_coordinates(database):
	try:
		# Connect to database
		connect = lite.connect(database)
		c = connect.cursor()
		# check if the sequence is even within the size of the sql table.
		c.execute('SELECT COUNT(*) FROM ZMISSIONDATA;')
		# Due to the nature of the way the data is extracted from the SQL table 
		# this dirty data manipulation has to happen. It's just not elegant :(
		totalsequences = int(str(c.fetchone()).translate(None, "(),"))
		# Check the sequence number from user against total amount of sequences.
		if (int(sequence) < (totalsequences + 1)):
			# sqlite3 library documentation says it's more 'secure' to insert values into querys like so.
			t = (sequence,)
			c.execute('SELECT ZWP_WP_NR, ZWP_LAT, ZWP_LON FROM ZWAYPOINT WHERE ZMSD_SEQUENCE_NUMBER = ? ORDER BY ZWP_WP_NR ASC;', t)
			# Get the results of the query.
			coordinates = c.fetchall()
			# Again another issue, this time with data types. The sql query spits out a list of tuples.
			# the google maps api wants a list of lists....
			# We also want the waypoint number in there so you can hover over waypoint in the html file
			for x in range(0, len(coordinates)):
				coordinates[x] = list(coordinates[x])
				coordinates[x][0] = 'Waypoint: ' + str(coordinates[x][0])
			# Finally return the results to wherever this function was called from
			return coordinates
		else:
			# Error out of bounds readout.
			print 'This table has', totalsequences, 'total sequences. Try execution with a different number.'
			exit(0)
	# If the file can't be read/corrupted/whatever else we should hopefully be able to debug with the error message.
	except IOError, e:
		print 'File error:', e
		exit(0)
		
def get_alert(database):
	try: 
		# Connect to database
		connect = lite.connect(database)
		c = connect.cursor()
		# Get the UUID that relates all the data to a device with the same UUID (experiments have proved it to be the device is installed on, a tablet for example.)
		c.execute("SELECT Z_UUID FROM Z_METADATA;")
		# Fetchone seems to grab an item from the table and I guess turn it into a string IF there is one element to it.
		uuidStr = str(c.fetchone())
		# Had to cast the above line to a string and format the string, I feel dirty for doing so but deadlines and stuff.
		uuid = uuidStr.translate(None, "',()u")
		# We also need the time of flight from the database.
		#t = ... line is apparently a more secure way to input a value into an SQL qeurey (querey?)
		t = (sequence,)
		c.execute('SELECT ZMSD_TIME_INTERVAL_SINCE_1970 FROM ZMISSIONDATA WHERE ZSEQUENCE_NUMBER = ?;', t)
		timeinsecondsStr = str(c.fetchone()).translate(None, "(),")
		#So to do the formatting of certain acharacters I no have to turn it back to an int. This is rapidly becoming unorganised, need to fix.
		timeinseconds = float(timeinsecondsStr)
		#from import datetime library you can simply convert seconds elapsed from 1/1/1970 to get a date. Which is what we are doing here.
		date = datetime.fromtimestamp(timeinseconds)
		# Finally we return the string of relevant info that'll eventually be inserted into the alert box.
		get_alertOutput = "Sequence: " + str(sequence) + "<br><br>Flown on: " + str(date) + "<br><br>UUID: " + str(uuid)
		return get_alertOutput
	except:
		return 'Could not retrieve either UUID or date from database.'

# Here we change the formatting of the waypoints so gmaps api can use them to plot lines
def make_points(coords):
	if(coords):
		# Firstly we don't need the way point number in this as we already have our waypoints in order.
		for x in range(0, len(coords)):
			if(len(coords[x]) > 2):
				coords[x].pop(0)
		
		# List comprehensions are fun. Basically telling it the format I want and then it has its 
		# own little for loop and then changes all elements. It's more obvious when you look at
		# var points in a generated html file.
		new_list = [{'lat': d[0], 'lng': d[1]} for d in coords]
		# Return the new list after the list comprehension.
		return new_list
	else:
		print 'parameter was dodgy.'



##################################################
#                                                #
#       Create html using the following:         #
#                                                #
##################################################
# Map title is the text in the tab on whatever browser
map_title = 'Sequence ' + str(sequence)

# This gets the coordinates from the above function 
gps_markers = get_coordinates(db) 

gpslines = [sublist[:] for sublist in gps_markers]
# This gets the information to display in the alert pop up box
alert = get_alert(db)
# This will take the points and make sure they can be used to make lines on the map
plots = make_points(gpslines)
# Here we generate the html page by passing the above 
# information to the relevant files
example_map = simplemap.Map(map_title, markers=gps_markers, message=alert, points=plots)
# We also need a name for the html file that's being outputted
example_map.write('sequence' + str(sequence) + '.html')

# Finally we finish the script by opening the html
# file with whatever is the defult browser
webbrowser.open_new('sequence' + str(sequence) + '.html')

# Give some indication that the process has finished and now we just open the html file.
print '\nOpening sequence' + str(sequence) + '.hmtl...'
