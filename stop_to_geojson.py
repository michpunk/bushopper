#!/usr/bin/python
import math
import sys
from geojson import Feature, Point, FeatureCollection
import geojson

def json_dump(bus_stops_file, coord_file, outfile='stops.geojson'):
  fn = coord_file
  Flist = []
  stop_names = {}
  with open(bus_stops_file, 'r') as f:
    f.readline()
    for line in f:
      s  = line.split(',')
      if len(s) == 3:
        l1 = f.next()
        tmp = line+l1
        s = tmp.split(',')
      assert(len(s) == 9)
      stop_id = s[0]
      name = s[3]
      stop_names[stop_id] = name
  with open(fn, 'r') as f:
    for l in f:
      line = l.split(',')
      coords = (float(line[5]), float(line[4]))
      my_Point = Point(coords)
      Flist.append(Feature(geometry=my_Point, id=line[0],properties={"name": stop_names[line[0]]}))
  FC = FeatureCollection(Flist)
  with open(outfile, 'w') as outfile:
    geojson.dump(FC, outfile)

def main():
  json_dump(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__=="__main__":
  main()
