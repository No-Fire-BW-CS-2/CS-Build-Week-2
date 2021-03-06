from urls import post, get, end
from util import Graph
from mine import mine
import json
import os

global data
data = get(end['init'])

global snitch
snitch = False if data['room_id'] < 500 else True

gr = Graph()
map_file = 'map.json' if snitch == False else 'map2.json'
with open(map_file) as map:
    completed_map = json.load(map)
    for room in completed_map:
        if completed_map[room] == data['room_id']:
            data = completed_map[room]
        gr.add_vertex(completed_map[room])


def exits():
    global data
    all_exits = data['exits']
    print('Exits: [', end='')
    for i, x in enumerate(all_exits):
        room_id = gr.rooms[data['room_id']]['exits'][x]
        room_title = gr.rooms[room_id]['title']
        terrain = gr.rooms[room_id]['terrain']
        if i + 1 == len(all_exits):
            print(f'{x} ({room_id} - {room_title} [{terrain}])', end='')
        else:
            print(f'{x} ({room_id} - {room_title} [{terrain}])', end=', ')
    print(']')


def print_room(room):
    room_id = room['room_id']
    title = room['title']
    description = room['description']
    players = room['players']
    items = room['items']
    exits = room['exits']
    messages = room['messages']
    print(f'Room {room_id} - {title}:\n\t{description}')
    if len(players):
        print('Players in room:')
        for player in players:
            print(f'\t{player}')
    if len(items):
        print('Items in room:')
        for item in items:
            print(f'\t{item}')
    if len(messages):
        print('Messages:')
        for message in messages:
            print(f'\t{message}')
    print('Exits: [', end='')
    for i, x in enumerate(exits):
        room_id = gr.rooms[room['room_id']]['exits'][x]
        room_title = gr.rooms[room_id]['title']
        terrain = gr.rooms[room_id]['terrain']
        if i + 1 == len(exits):
            print(f'{x} ({room_id} - {room_title} [{terrain}])', end='')
        else:
            print(f'{x} ({room_id} - {room_title} [{terrain}])', end=', ')
    print(']')


def print_info(request):
    print(json.dumps(request, indent=2))


def get_req(endpoint):
    req = get(end[endpoint])
    print_info(req)


def post_req(endpoint):
    req = post(end[endpoint], {})
    if endpoint == 'warp':
        global snitch
        snitch = True if snitch == False else False
        print_room(req)
    else:
        print_info(req)


def travel(room_id):
    global data
    data = get(end['init'])
    travelled = gr.get_path_to_room(data, int(room_id))
    print_room(travelled)
    data = travelled
    return travelled


def well():
    global snitch
    well_num = 55 if not snitch else 555
    return travel(well_num)


def shop():
    travel(1)
    status = post(end['status'], {})
    inventory = status['inventory']
    while len(inventory):
        print(inventory)
        post(end['sell'], {"name": "treasure"})
        post(end['sell'], {"name": "treasure", "confirm": "yes"})
        status = post(end['status'], {})
        inventory = status['inventory']


def move(direction):
    global data
    room_in_dir = gr.rooms[data['room_id']]['exits'][direction]
    moved = post(end['move'], {
        'direction': direction,
        'next_room_id': str(room_in_dir)
    })
    print_room(moved)
    data = moved
    return moved


def examine(target):
    examined = post(end['examine'], {'name': target})
    print_info(examined)
    if target == 'well':
        ls8 = examined['description'][39:].split('\n')
        with open('ls8.ls8', 'w') as ls:
            ls.truncate()
            for line in ls8:
                if line != '':
                    json.dump(int(line), ls)
                    ls.write('\n')
        os.system('python ls8.py ls8.ls8')
        with open('room.ls8') as room_file:
            return travel(room_file.read())
    return examined


def mine_loop():
    while True:
        global data
        data = well()
        data = examine('well')
        mine()
        get_req('bal')


def take(target):
    taken = post(end['take'], {'name': target})
    print_room(taken)
    return taken


def transmogrify(item):
    mog = post(end['change'], {'name': item})
    get_req('status')
    print_room(mog)
    return mog


global cmds
cmds = {
    'mine': mine_loop,
    'well': well,
    'exits': exits,
    'shop': shop,
    'self': {
        'bal': get_req,
        'status': post_req,
        'warp': post_req,
        'pray': post_req,
    },
    'double': {
        'travel': travel,
        'move': move,
        'examine': examine,
        'take': take,
        'mog': transmogrify,
    }
}

instructions = f'''
Command options:
\tMine (begins mining for a coin)
\tPray (you pray in this room)
\tTravel <room> (begins a journey to <room> number)
\tExits (prints the exits in current room)
\tMove <direction> (will move you in the direction specified)
\tStatus (shows your character's status)
\tShop (begins journey to shop)
\tWell (begins a journey to the well)
\tBal (shows your current coin balance)
\tExamine <target> (examines the specified target - can be player or item)
\tRoom (shows details of current room)
\tTake <target> (picks up an item)
\tMog <item> (transmogrify <item>)
\tWear <item> (wear <item>)
\tUndress <item> (unwear <item>)
\tCarry <target> (TBD)
\tWarp (warp to alternate dimension)
\tHelp (print these instructions again)
'''

print(instructions)

crashed = False
while not crashed:
    cmd = input(f'What would you like to do? ').lower()

    command = cmd.split(' ')

    if len(command) == 1:
        if cmd == 'room':
            print_room(data)
        elif cmd in cmds:
            cmds[cmd]()
        elif cmd in cmds['self']:
            res = cmds['self'][cmd](cmd)
        elif cmd == 'help':
            print(instructions)
        else:
            print(f'Command "{cmd}" not recognized.')

    elif command[0] in cmds['double']:
        cmds['double'][command[0]](command[1])

    elif command[0] == 'wear':
        item = ' '.join(command[1:])
        wear = post(end['wear'], {'name': item})
        print_info(wear)

    elif command[0] == 'undress':
        item = ' '.join(command[1:])
        undress = post(end['undress'], {'name': item})
        print_info(undress)

    else:
        print(f'Wtf is {cmd}?')
