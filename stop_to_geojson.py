#!/usr/bin/python
import math
import sys
from geojson import Feature, Point, FeatureCollection
import geojson

def json_dump(coord_file, dists, outfile='stops.geojson'):
  fn = sys.argv[1]
  Flist = []
  with open(fn, 'r') as f:
    for l in f:
      line = l.split(',')
      coords = (float(line[5]), float(line[4]))
      my_Point = Point(coords)
      Flist.append(Feature(geometry=my_Point, id=line[0],properties={"distance": dists[line[0]]}))
  FC = FeatureCollection(Flist)
  with open(outfile, 'w') as outfile:
    geojson.dump(FC, outfile)

if __name__=="__main__":
  main()
