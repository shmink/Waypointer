#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author Tom Nicklin

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

# In an effor to make this system more modular the user passes in a sequence number and table for the waypoints.
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
def getcoordinates(database):
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
		if (int(sequence) < totalsequences):
			# sqlite3 library documentation says it's more 'secure' to insert values into querys like so.
			t = (sequence,)
			c.execute('SELECT ZWP_LAT, ZWP_LON FROM ZWAYPOINT WHERE ZMSD_SEQUENCE_NUMBER = ?;', t)
			# Get the results of the query.
			coordinates = c.fetchall()
			# Again another issue, this time with data types. The sql query spits out a list of tuples.
			# the google maps api wants a list of lists....
			for x in range(0, len(coordinates)):
				coordinates[x] = list(coordinates[x])
			# Finally return the results to wherever this function was called from
			return coordinates
		else:
			# Error out of bounds readout.
			print 'This table has', totalsequences, 'total sequences. Try execution with a different number.'
			exit(0)
	# If the file can't be read/corrupted/whatever else we should hopefully be able to debug with the error message.
	except IOError, e:
		print 'File error:', e
		

##################################################
#												 #
#       Create html using the following:         #
#                                                #
##################################################
# Map title is the text in the tab on whatever browser
map_title = 'Sequence ' + str(sequence)

# This gets the coordinates from the above function 
gps_markers = getcoordinates(db) 

# Here we generate the html page by passing the above 
# information to the relevant files
example_map = simplemap.Map(map_title, markers=gps_markers)
# We also need a name for the html file that's being outputted
example_map.write('sequence' + str(sequence) + '.html')

# Finally we finish the script by opening the html
# file with whatever is the defult browser
webbrowser.open_new('sequence' + str(sequence) + '.html')