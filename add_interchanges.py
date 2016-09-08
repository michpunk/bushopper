def add_interchanges(stops, adj_lists, neighb):
  for stop in stops:
    tmp = set([])
    for stop2 in adj_lists[stop]:
      tmp.update(neighb[stop2])
    adj_lists[stop].update(tmp)

