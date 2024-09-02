######################################################################
# Author: Sullyandro Guimaraes
# E-mail: sullyandro@gmail.com
# Date:   01.10.2024
#
# Script: 
# - Convert asc to shp of points, of polygon, and simplify the polygon
# - And extract asc from simplified polygon
######################################################################

import os
import math
import shapefile
import numpy as np
import pandas as pd 
import geopandas as gpd 
import matplotlib as mpl #; mpl.use('Agg') # uncomment here to not show the plot window
import matplotlib.pyplot as plt
from   shapely.geometry import Point, Polygon


# Read the CSV file 

# file: 1_acarau_mirim.asc

# Content: longitude,latitude
#
# -40.414760860,-3.609036450
# -40.415868360,-3.609312790
# -40.416145550,-3.609590420
# -40.416976280,-3.609867180
# -40.417253480,-3.610144810
# -40.417807450,-3.610422010
# ...

csv_file = './1_acarau_mirim.asc' 

pd_data = pd.read_csv(csv_file, names=['longitude','latitude']) 


# Plot
csv_figu = './1_acarau_mirim.png' 
plt.figure(figsize=(6,6))
plt.plot(pd_data.longitude, pd_data.latitude, 'o-', markersize=3, color='red')
plt.title(csv_file.split('/')[-1])
plt.savefig(csv_figu, bbox_inches='tight', dpi=70, transparent=True)
plt.close()
if os.path.exists(csv_figu): print('done -->', csv_figu)


# Create a function to create Point objects from coordinate pairs 
def create_point(row): 

	return Point(row['longitude'], row['latitude']) 
		
		
# Apply the function to create a new 'geometry' column containing Point objects 

pd_data['geometry'] = pd_data.apply(create_point, axis=1) 


# Convert the DataFrame to a GeoDataFrame (gdf) and set the CRS 

gdf = gpd.GeoDataFrame(pd_data, crs="EPSG:4326") 


# Save the GeoDataFrame as a shapefile - This shape will contain the points, not the polygon yet

output_shapefile_points = './1_acarau_mirim_shape_with_points.shp' 

gdf.to_file(output_shapefile_points)

if os.path.exists(output_shapefile_points): print('done -->', output_shapefile_points)


# Creating the Polygon from the shape points

poly = Polygon([[p.x, p.y] for p in pd_data.geometry])

# Save the GeoDataFrame as a shapefile - This shape will contain the polygon

output_shapefile_polygon = './1_acarau_mirim_shape_with_polygon.shp' 

# add crs using wkt or EPSG to have a .prj file

gdr = gpd.GeoDataFrame({'feature':[0], 'geometry':poly}, crs='EPSG:4326')

gdr.to_file(output_shapefile_polygon)

if os.path.exists(output_shapefile_polygon): print('done -->', output_shapefile_polygon)


# Making a simplification on the polygon to later on create a asc with less points and make thiessen routing run faster

poly_s = poly.simplify(tolerance=0.001)

# Save the GeoDataFrame as a shapefile - This shape will contain the polygon simplified

output_shapefile_polygon_simp = './1_acarau_mirim_shape_with_polygon_simp.shp' 

# add crs using wkt or EPSG to have a .prj file

gdr_s = gpd.GeoDataFrame({'feature':[0], 'geometry':poly_s}, crs='EPSG:4326')

gdr_s.to_file(output_shapefile_polygon_simp)

if os.path.exists(output_shapefile_polygon_simp): print('done -->', output_shapefile_polygon_simp)



# Converting the simplified shape to asc

shp_name = output_shapefile_polygon_simp
asc_name = output_shapefile_polygon_simp[0:-4]+'.asc'
fig_name = output_shapefile_polygon_simp[0:-4]+'.png'

# Reading shp
sf = shapefile.Reader(shp_name, encodingErrors="replace")
geo = sf.shapeRecords()        # get the geometry 
feat_num = geo[0]              # if it is only one polygon, then 0. if multipolygon, then check the range
coords = feat_num.shape.points # show the points extracted from the polygon
coords = np.array(coords)

# Saving asc
np.savetxt(asc_name, coords, delimiter=',',fmt='%1.9f')
if os.path.exists(asc_name):
	print('done -->', asc_name)

# Plot
plt.figure(figsize=(6,6))
plt.plot(coords[:,0], coords[:,1], 'o-', markersize=3)
plt.title(asc_name.split('/')[-1])
plt.savefig(fig_name, bbox_inches='tight', dpi=70, transparent=True)

# plt.show()
plt.close()
if os.path.exists(fig_name):
	print('done -->', fig_name)








