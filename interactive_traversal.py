from urls import post, get, end
from util import Graph
from mine import proof_of_work
import json
import os
"""
1. pick up treasure
2. sell treasure (up to 1000 gc)
3. change name
4. get location from well
5. go to location from well, start mining
"""


"""
gold, encumbrance, strength = post(get gold, encumbrance, strength)
while gold < 1000:
  while encumbrance < strength:
    traverse and pick up treasure
    gold, encumbrance, strength = post(get gold, encumbrance, strength)
  go to shop, sell treasure
  gold, encumbrance, strength = post(get gold, encumbrance, strength)

go to namechanger, change name
"""
# gr = None

# for room in gr:
#   print(room['items'])

data = get(end['init'])
# print(data)
gr = Graph()
# gr.add_vertex(data)

with open('map.json') as map:
    completed_map = json.load(map)
    for room in completed_map:
        if completed_map[room] == data['room_id']:
            data = completed_map[room]
        gr.add_vertex(completed_map[room])
# print(gr.rooms)
# print(gr.rooms[325]['room_id'], gr.rooms[325]['exits'])
# quit()

status = post(end['status'], {})
inventory = status['inventory']
gold = int(status['gold'])
name = status['name']
encumbrance = int(status['encumbrance'])
strength = int(status['strength'])
# print(gold)
if status['name'][:4] == 'User':
    rooms_with_items = []
    for room_id, room in gr.rooms.items():
        if len(room['items']):
            rooms_with_items.append(room_id)
    while gold < 1000:
        while encumbrance < strength:
            item_room = rooms_with_items.pop()
            room_with_item = gr.get_path_to_room(data, item_room)
            if len(room_with_item['items']):
                take_item = post(
                    end['take'], {'name': room_with_item['items'][0]})
                gr.rooms[item_room]['items'] = []
                status = post(end['status'], {})
                gold = int(status['gold'])
                encumbrance = int(status['encumbrance'])
                strength = int(status['strength'])
            print("current room ---->", data)
        print(data)
        # 1 is the shop
        path = gr.get_path_to_room(data, 1)
        print("path -------------->", path)
        while len(inventory) > 0:
          post(end['sell'], {"name":"treasure"})
          post(end['sell'], {"name":"treasure", "confirm": "yes"})
          status = post(end['status'], {})
          inventory = status['inventory']
          gold = int(status['gold'])
          encumbrance = int(status['encumbrance'])
          print("Status", status)
  # 467 
    path = gr.get_path_to_room(data, 467)
    print("path to namechanger --------->", path)
    name = input("What is your name? ")
    res = post(end['name'], {"name": f"{name}"})
    confirm = post(end['name'], {"name": f"{name}", "confirm": "aye"})
    # print(confirm)
    # status = post(end['status'], {})
    # print(status)
if status['name'][:4] != 'User':
    while True:
        to_go = int(input('Which room would you like to go to? '))
        to_go_room = gr.get_path_to_room(data, to_go)
        data = to_go_room
        balance = get(end['bal'])
        print('balance ---->', balance)
        if to_go == 55:
            examine = post(end['examine'], {'name': 'well'})
            print('examine well ---->', examine)
            ls8 = examine['description'][39:].split('\n')
            with open('ls8.ls8', 'w') as ls:
                ls.truncate()
                for line in ls8:
                    if line != '':
                        json.dump(int(line), ls)
                        ls.write('\n')
            os.system('python ls8.py ls8.ls8')
        else:
            mining = True
            while mining:
                last_proof = get(end['lp'])
                next_proof = proof_of_work(last_proof)
                check_proof = post(end['mine'], {'proof': next_proof})
                mine_status = post(end['status'], {})
                print('mine_status ---->', mine_status)
                balance = get(end['bal'])
                print('balance ---->', balance)
                if not len(check_proof['errors']):
                    mining = False
