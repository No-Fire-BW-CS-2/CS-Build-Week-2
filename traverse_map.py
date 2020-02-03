import json
import requests
from urls import base, end, post, get
import os

# importing token and init endpoint

# auth header 

# init endpoint - loads current room
data = get(end['init'])
print(data)


map_data = {}

map_data[data['room_id']] = data

print("map_data", map_data)
 
"""
{room_id: {title: "foo", terrain: "bar"}}
"""






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
'players': ['User 20498', 'User 20493', 'User 20500', 'User 20501', 'User 20502', 'brady - cs24', 'User 20503', 'User 20505', 'User 20507', 'User 20471', 'User 20508', 'User 20472', 'User 20504', 'User 20474', 'User 20509', 'User 20510', 'User 20477', 'User 20511', 'User 20478', 'User 20512', 'User 20479', 'User 20480', 'User 20513', 'User 20481', 'User 20514', 'User 20567', 'User 20483', 'User 20484', 'User 20515', 'User 20485', 'User 20486', 'User 20516', 'User 20487', 'User 20517', 'User 20488', 'User 20489', 'User 20518', 'User 20490', 'User 20519', 'User 20491', 'User 20492', 'User 20521', 'User 20494', 'User 20495', 'User 20496', 'User 20497', 'User 20523', 'User 20526', 'User 20525', 'User 20527', 'User 20528', 'User 20529', 'User 20580', 'User 20530', 'User 20531', 'User 20532', 'User 20533', 'User 20534', 'User 20535', 'User 20536', 'User 20541', 'User 20538', 'User 20581', 'User 20539', 'User 20540', 'User 20542', 'User 20543', 'User 20473', 'User 20546', 'User 20547', 'User 20548', 'User 20549', 'User 20550', 'User 20551', 'User 20552', 'User 20553', 'User 20555', 'User 20556', 'User 20558', 'User 20559', 'User 20560', 'User 20561', 'User 20562', 'User 20563', 'User 20565', 'User 20566', 'User 20568', 'User 20537', 'User 20569', 'User 20570', 'User 20571', 'User 20572', 'User 20573', 'User 20574', 'User 20575', 'User 20576', 'User 20577', 'User 20506', 'User 20475'], 
'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 1.0, 
'errors': [], 'messages': []}'''