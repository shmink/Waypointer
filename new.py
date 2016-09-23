#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Tom Nicklin

from datetime import datetime
import simplemap
import sqlite3 as lite
import webbrowser
import sys
import os

#This will be passed in as the second parameter when running the script
db = ''
#uuid needed from z_metadata
uuid = ''
#sequence number needed from user
sequence = 0
#timeinseconds is from zmsd_time_interval_since_1970 from zmissondata, it's elapsed seconds since 1/1/1970
timeinseconds = 0

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
	else:
		print 'The format required is `python test.py <sequence number> <sqlite file>`'
		exit(0)

def getcoordinates(database):
	try:
		connect = lite.connect(database)
		c = connect.cursor()
		t = (sequence,)
		c.execute('SELECT ZWP_LAT, ZWP_LON FROM ZWAYPOINT WHERE ZMSD_SEQUENCE_NUMBER = ?;', t)
		coordinates = c.fetchall()

		for x in range(0, len(coordinates)):
			coordinates[x] = list(coordinates[x])

		return coordinates

	except IOError, e:
		print 'File opening error:', e
		

##################################################
#												 #
#       Create html using the following:         #
#                                                #
##################################################
# Map title is the text in the tab on whatever browser
map_title = 'Sequence ' + str(sequence)

# This gets the coordinates from the above function 
gps_markers = getcoordinates('db') 

# Here we generate the html page by passing the above 
# information to the relevant files
example_map = simplemap.Map(map_title, markers=gps_markers)
# We also need a name for the html file that's being outputted
example_map.write('sequence' + str(sequence) + '.html')

# Finally we finish the script by opening the html
# file with whatever is the defult browser
webbrowser.open_new('sequence' + str(sequence) + '.html')