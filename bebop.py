#!/usr/bin/python
"""
Take the csv file created and then take legitimate waypoints and plot 
them on google maps using their api.

@autoher: Tom Nicklin
"""
# Import the pud to csv class and refer to is as pud for ease.
import pudconverter
from datetime import datetime
import json
import csv
import simplemap
import webbrowser
import sys
import os

pudfile = ''

# In an effort to make this system more modular the user passes in a sequence number and table for the waypoints.
# this is that argument system. It still doesn't seem right to me but I've tested it enough that it works.
if __name__ == '__main__':
	if len(sys.argv) == 2:
		if os.path.isfile(sys.argv[1]):
			pudfile = sys.argv[1]
		else:
			print 'File could not be found.'
			exit(0)
	else:
		print 'The format required is `python bebop.py <pud file>'
		exit(0)

def send_to_converter(myFile):
	os.system('python pudconverter/pud_to_csv_kml.py ' + pudfile)
	print 'Converting your .pud file...'
	csvfile = pudfile + '.csv'
	print csvfile

send_to_converter(pudfile)

def get_coordinates(file):
	with open(file, 'rb') as csvfile:

		# printing specifics
		readmorelikecashmore = csv.DictReader(csvfile)


		coordinates = [ [ 'altitude: ' + row['altitude'] + 'cm, flying state: ' + row['flying_state'], float(row['product_gps_latitude']), float(row['product_gps_longitude']) ] for row in readmorelikecashmore]
		
		# When we get the gps coordinates, some of them are 500. That doesn't exist on maps, as a result gmaps just doesn't function.
		# Here we santise (ignore) those results.
		sanitised = []
		for x in range(0, len(coordinates)):
			# If legitimate gps locations then the following if should be true.
			if((coordinates[x][1] or coordinates[x][2]) < 180):
				sanitised.append(coordinates[x])
		# Finally we return the result.
		return sanitised

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

def get_header_info(file):
	try:
		contents = open(file, 'rb').read()

		# Extract the JSON header.
		null_terminator_index = contents.index('\x00')
		header_json = contents[:null_terminator_index]
		packets = contents[null_terminator_index+1:]

		# Parse the header.
		header = json.loads(header_json)
		date = header['date']
		dateformatted = datetime.strptime(date[:17],"%Y-%m-%dT%H%M%S")
		product_id = header['product_id']
		serial_number = header['serial_number']
		hardware_version = header['hardware_version']
		software_version = header['software_version']
		uuid = header['uuid']
		controller_model = header['controller_model']
		controller_application = header['controller_application']
		product_style = header['product_style']
		product_accessory = header['product_accessory']

		# A big old message for the output.
		output = "Date as saved: " + str(date) + "<br><br>Date formatted: " + str(dateformatted) + "<br><br>Product ID: " + str(product_id) + "<br><br>Serial Number: " + str(serial_number) + "<br><br>Hardware Version: " + str(hardware_version) + "<br><br>Software Version: " + str(software_version) + "<br><br>UUID: " + str(uuid) + "<br><br>Controller Model: " + str(controller_model) + "<br><br>Controller Application: " + str(controller_application) + "<br><br>Product Style: " + str(product_style) + "<br><br>Product Accessory: " + str(product_accessory)
		return output

	except IOError, e:
		print 'File error:', e
		exit(0)

	



##################################################
#                                                #
#       Create html using the following:         #
#                                                #
##################################################
# Map title is the text in the tab on whatever browser
map_title = pudfile

# This gets the coordinates from the above function 
gps_markers = get_coordinates(pudfile + '.csv')

# We need a clone of gps_markers because python assigns by reference. 
# In short it means if you change the copy you'll ALSO change the original. Not good. 
# On top of that gps_markers is a 2D list so it requires a bit more thought.
new_gps = [sublist[:] for sublist in gps_markers]

# Use said copy to do something different without effecting the original.
plots = make_points(new_gps)

# Get header info in the form of a string that we can then send as a message to the webpage
alert = get_header_info(pudfile)

# Here we generate the html page by passing the above 
# information to the relevant files
example_map = simplemap.Map(map_title, markers=gps_markers, points=plots, message=alert)
# We also need a name for the html file that's being outputted
example_map.write(pudfile + '.html')

# Finally we finish the script by opening the html
# file with whatever is the defult browser
webbrowser.open_new(pudfile + '.html')

# Give some indication that the process has finished and now we just open the html file.
print '\nWriting ' + pudfile + '.hmtl...'