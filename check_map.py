import json
gr = {}
with open('map.json') as completed_map:
  gr = json.load(completed_map)

reverse_dirs = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

def check_map():
  mismatches = []
  for room in gr:
    exits = gr[room]['exits']
    for neighbor in exits.values():
      neighbor_room = gr[str(neighbor)]
      if int(room) not in neighbor_room['exits'].values():
        mismatches.append({'room': room, neighbor: str('neighbor')})
  return mismatches

print(check_map())