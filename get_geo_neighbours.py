#!/usr/bin/python
import math

def gridDistance(ref1, ref2):
  deltaE = int(ref2[0])-int(ref1[0])
  deltaN = int(ref2[1])-int(ref1[1])

  dist = math.sqrt(deltaE*deltaE + deltaN*deltaN)
  return dist/1000

def get_cand_buckets(cb):
  cands = []
  for i in [cb[0]-1,cb[0],cb[0]+1]:
    for j in [cb[1]-1,cb[1],cb[1]+1]:
      cands.append((i,j))
  return cands


def get_stops_and_interchanges(filename):
  buckets = {}
  neighb = {}
  stops = {}
  with open(filename, 'r') as f:
    f.readline()
    for line in f:
      s  = line.split(',')
      if len(s) == 3:
        l1 = f.next()
        tmp = line+l1
        s = tmp.split(',')
      assert(len(s) == 9)
      stop_id = s[0]
      cb = (int(s[4][:-3]), int(s[5][:-3]))
      if cb in buckets:
        buckets[cb].append(stop_id)
      else:
        buckets[cb] = [stop_id]
      stops[stop_id] = (s[4], s[5])

  #now -- neighbours..
  for stop in stops:
    coords = stops[stop]
    cb = (int(coords[0][:-3]),int(coords[1][:-3]))
    neighb[stop] = []
    bucks = get_cand_buckets(cb)
    for b in bucks:
      if b in buckets:
        cand_stops = buckets[b]
        for s in cand_stops:
          if gridDistance(coords, stops[s]) < 0.3 and s != stop:
            neighb[stop].append(s)
  return (stops, neighb)
