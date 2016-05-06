"""
Given an input shapefile, extract centroids of polygons inside it
and tag them with one of the properties.

For example:
python geoscripts/shapefile_to_centroid.py Parcel.shp out.csv --projection 2227 --property_name APN

prints out all the centroids for polygons in Parcel.shp to out.csv.
Assuming, of course, that Parcel.shp is in EPSG 2227
"""

import csv
import fiona
import pyproj
import argparse
from shapely.geometry import shape

def run(filename, outfile, property_name, projection=2227):
    projector = pyproj.Proj(init='epsg:{}'.format(projection),
                            preserve_units=True)
    centroid_data = []
    with fiona.open(filename) as source:
        for poly in source:
            geom = shape(poly['geometry'])
            id_key = poly['properties'][property_name]
            longitude, latitude = projector(geom.centroid.coords[0][0],
                                            geom.centroid.coords[0][1],
                                            inverse=True)
            centroid_data.append((id_key, latitude, longitude))

    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([property_name, 'latitude', 'longitude'])
        for datum in centroid_data:
            writer.writerow(datum)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Process a shapefile')
    parser.add_argument('filename', type=str,
                        help='Path to shapefile to process')
    parser.add_argument('outfile', type=str,
                        help='Path to output CSV')
    parser.add_argument('--property_name', type=str,
                        default='APN',
                        help='Entry in properties we use for ID')
    parser.add_argument('--projection', type=int,
                        default=2227,
                        help='EPSG projection if necessary')
    args = parser.parse_args()
    run(filename=args.filename,
        outfile=args.outfile,
        property_name=args.property_name,
        projection=args.projection)
