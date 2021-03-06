#!/usr/bin/python
import math
import sys
import time
#from geojson import Feature, Point, FeatureCollection
#import geojson
import json
from get_geo_neighbours import get_stops_and_interchanges
from process_routes import process_routes
from add_interchanges import add_interchanges

#buckets = {}
#stops = {}
#neighb = {}
#adj_lists = {}

def findmin(Q, dist):
  m = float('inf')
  for stop in Q:
    if dist[stop] <= m:
      m = dist[stop]
      cand = stop
  return cand

def dijkstra(adj_lists, stops, neighb, source):
    Q = set(stops)
    dist = {}
    prev = {}

    for stop in stops:
      if stop != source:
        dist[stop] = float('inf')
        prev[stop] = {}
    dist[source] = 0
    for stop in neighb[source]:
      dist[stop] = 0

    while len(Q) > 0:
      u = findmin(Q, dist)
      Q.remove(u)
      for n in adj_lists[u]:
        alt = dist[u] + 1
        if alt < dist[n]:
          dist[n] = alt
          prev[n] = u
    return dist

def cheat_dijkstra(adj_lists, stops, neighb, source):
  dist = {}
  dist[source] = 0
  for stop in neighb[source]:
    dist[stop] = 0
  d1 = set(adj_lists[source])
  for stop in neighb[source]:
    d1.update(adj_lists[stop])
  for stop in d1:
    if stop not in dist:
      dist[stop] = 1;
  for stop1 in d1:
    for stop2 in adj_lists[stop1]:
      if stop2 not in dist:
        dist[stop2] = 2
  return dist

def json_dump(coord_file, dists):
  fn = coord_file
  Flist = []
  with open(fn, 'r') as f:
    for l in f:
      line = l.split(',')
      coords = (float(line[5]), float(line[4]))
      my_Point = Point(coords)
      d = dists[line[0]]
      if d > 100:
        d = -1
      Flist.append(Feature(geometry=my_Point, id=line[0],properties={"distance": d}))
  FC = FeatureCollection(Flist)
  with open('stops.geojson', 'w') as outfile:
    geojson.dump(FC, outfile)

def dict_dump(dict_file, d):
  with open(dict_file, 'w') as outfile:
    outfile.write('var distDict = ')
    json.dump(d, outfile)
    outfile.write(';')


def main(argv):
  (stops, neighb) = get_stops_and_interchanges(argv[1])
  adj_lists = process_routes(argv[2], stops)
  datadir = argv[3]
  add_interchanges(stops, adj_lists, neighb)
  t = time.time()
#  d = cheat_dijkstra(adj_lists, stops, neighb, 'RTP117')
  for stop in stops:
    d = cheat_dijkstra(adj_lists, stops, neighb, stop)
    dict_dump(datadir+stop+'-cheat.js',d)
  elapsed = time.time() - t
  print "Elapsed time: " + str(elapsed)
  #json_dump('./bus_stops_coords.csv',d)

if __name__ == "__main__":
  main(sys.argv)
