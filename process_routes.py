def process_route(route, adj_lists):
  for i, stop in enumerate(route):
    adj_lists[stop].update(route[(i+1):])

def import_routes(filename):
  routes = {}
  with open(filename, 'r') as f:
    f.readline()
    for line in f:
      s  = line.split(',')
      if len(s) == 6:
        l1 = f.next()
        tmp = line+l1
        s = tmp.split(',')
      assert(len(s) >= 11 and len(s) <=12)
      route = s[0]+"_"+s[1];
      if route in routes:
        routes[route].append(s[3])
      else:
        routes[route] = [s[3]]
  return routes

def process_routes(filename, stops):
  adj_lists = {}
  routes = import_routes(filename)
  for stop in stops:
    adj_lists[stop] = set()
  for route in routes:
    if route[0] != 'N':
      process_route(routes[route], adj_lists)
  #print len(adj_lists['34323'])
  #print len(adj_lists['34323'])
  return adj_lists
