import csv
import simplemap
import webbrowser

csvfile = 'test3.pud.csv'

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
			if((coordinates[x][1] or coordinates[x][2]) < 179):
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

	



##################################################
#                                                #
#       Create html using the following:         #
#                                                #
##################################################
# Map title is the text in the tab on whatever browser
map_title = csvfile

# This gets the coordinates from the above function 
gps_markers = get_coordinates(csvfile)

# We need a clone of gps_markers because python assigns by reference. 
# In short it means if you change the copy you'll ALSO change the original. Not good. 
# On top of that gps_markers is a 2D list so it requires a bit more thought.
new_gps = [sublist[:] for sublist in gps_markers]

# Use said copy to do something different without effecting the original.
plots = make_points(new_gps)


# Here we generate the html page by passing the above 
# information to the relevant files
example_map = simplemap.Map(map_title, markers=gps_markers, points=plots)
# We also need a name for the html file that's being outputted
example_map.write(csvfile + '.html')

# Finally we finish the script by opening the html
# file with whatever is the defult browser
webbrowser.open_new(csvfile + '.html')

# Give some indication that the process has finished and now we just open the html file.
print '\nWriting ' + csvfile + '.hmtl...'