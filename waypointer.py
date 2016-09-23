#!/usr/bin/python
# -*- coding: utf-8 -*-
#@author Tom Nicklin

from datetime import datetime
import sqlite3 as lite
import sys
import os
import webbrowser
import simplemap

#This will be passed in as the second parameter when running the script
db = ''
#uuid needed from z_metadata
uuid = ''
#sequence number needed from user
sequence = 0
#timeinseconds is from zmsd_time_interval_since_1970 from zmissondata, it's elapsed seconds since 1/1/1970
timeinseconds = 0
#use google maps api
#gmaps = googlemaps.Client(key='AIzaSyC74nEdTcDcoQhjLDTaa5JSU1ccmNqsA3E')
#now thinking of using this tool I found on github to save me a load of work. seems to work pretty simply which is nice

#For system arguments. Check the final print message for the format.
#Issue with which argument is what argument number.
if __name__ == '__main__':
	if len(sys.argv) == 3:
		#check if sequence number is an int
		if (sys.argv[1].isdigit()):
			sequence = sys.argv[1]
		else:
			print 'Use an actual number, not', sequence
		#check if file is there
		if os.path.isfile(sys.argv[2]):
			db = sys.argv[2]
		else:
			print 'File could not be found'
	else:
		print 'The format required is `python test.py <sequence number> <sqlite file>`'
		exit(0)

#Ideally could set this up so the file is passed in via parameters so it's way more modular.
#But this should take the final argument from terminal which should be an sql file.
connect = lite.connect(db)

#WITH the database connected (sql file) run the following code.
with connect:
    #Boiler plate connection stuff from what the documentation seem to say.
    c = connect.cursor()
    #Get the UUID that relates all the data to a device with the same UUID (proof more than anything.)
    c.execute("SELECT Z_UUID FROM Z_METADATA;")
    #Fetchone seems to grab an item from the table and I guess turn it into a string IF there is one element to it.
    uuidStr = str(c.fetchone())
    #Had to cast the above line to a string and format the string, I feel dirty for doing so but deadlines and stuff.
    uuidStr = uuidStr.translate(None, "',()u")

    #t = ... line is apparently a more secure way to input a value into an SQL qeurey (querey?)
    t = (sequence,)
    c.execute('SELECT ZMSD_TIME_INTERVAL_SINCE_1970 FROM ZMISSIONDATA WHERE ZSEQUENCE_NUMBER = ?;', t)
    timeinsecondsStr = str(c.fetchone()).translate(None, "(),")

    #So to do the formatting of certain acharacters I no have to turn it back to an int. This is rapidly becoming unorganised, need to fix.
    timeinseconds = float(timeinsecondsStr)

    #Pretty outputs for clear debugging
    print "\n=======Waypointer=======\n"

    #from import datetime library you can simply convert seconds elapsed from 1/1/1970 to get a date. Which is what we are doing here.
    date = datetime.fromtimestamp(timeinseconds)
    #Print out what we have in a nice format so that it's readable.
    print 'Sequence', sequence, 'was flown on:', date, '\n', 'its UUID that relates it to this table is:', uuidStr, '\n'

    #Need to get lat and long and feed into google maps api now.
    c.execute('SELECT ZWP_LAT, ZWP_LON FROM ZWAYPOINT WHERE ZMSD_SEQUENCE_NUMBER = ?;', t)
    coordinates = c.fetchall()

    #debugging tests below. above there is an indentation error.
    print 'coordinates variable is of type:', type(coordinates)
    print 'size of list of coordinates =', len(coordinates), '\n'

    for x in range(0, len(coordinates)):
    	print 'element', x, 'coordinates are:', coordinates[x]

    testCoor = coordinates[0]
    print 'testcoor is of type:', type(testCoor)

    testCoor = str(testCoor).strip('()')
    testCoor = testCoor.translate(None, " ")
    print 'stripping testcoor', testCoor
    #simple open up web brwoser command from importing 'webbrowser' library
    #webbrowser.open_new('https://www.google.co.uk/maps/@%s,17z' % testCoor)
