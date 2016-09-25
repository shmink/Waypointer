import simplemap

map_title = 'Example Map'
gps_markers = [ ['Example text', 34.4563,-118.1241], [34.6432,-118.1554] ]

#alerty = 'hi there' Testerino

example_map = simplemap.Map(map_title, markers=gps_markers)
example_map.write('example.html')
