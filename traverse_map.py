import json
import requests
from urls import base, end, post, get
import os
from util import Queue, Stack, Graph, reverse_dirs

# importing token and init endpoint

# auth header 

# init endpoint - loads current room
data = get(end['init'])


gr = Graph()    
gr.add_vertex(data)
print(gr.rooms)
map_data = {}

# map_data[data['room_id']] = data

# print("map_data", map_data)
 
"""
{room_id: {title: "foo", terrain: "bar"}}
"""
visited = set()
while len(visited) < 500:
    dfs = gr.dfs(data)





"""
After traversal
"""

with open('map.json', 'w') as outfile:
  json.dump(map_data, outfile)


'''
{'room_id': 0, 'title': 'A brightly lit room', 
'description': 'You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.',
'coordinates': '(60,60)', 
'elevation': 0, 'terrain': 'NORMAL', 
'players': [], 
'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 1.0, 
'errors': [], 'messages': []}'''