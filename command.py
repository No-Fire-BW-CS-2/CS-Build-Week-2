from urls import post, get, end
from util import Graph
from mine import mine
import json
import os

global data
data = get(end['init'])

gr = Graph()
with open('map.json') as map:
    completed_map = json.load(map)
    for room in completed_map:
        if completed_map[room] == data['room_id']:
            data = completed_map[room]
        gr.add_vertex(completed_map[room])


def pray():
    return post(end['pray'], {})


def exits():
    all_dirs = gr.get_all_directions(data)
    print('\nYou can move:', end=' ')
    for d in all_dirs:
        print(d, end=' ')
    print()


def print_room(room):
    room_id = room['room_id']
    title = room['title']
    description = room['description']
    players = room['players']
    items = room['items']
    exits = room['exits']
    messages = room['messages']
    print(f'Room {room_id} - {title}:\n\t{description}')
    print('Exits: [', end='')
    for i, x in enumerate(exits):
        global data
        room_id = gr.rooms[room['room_id']]['exits'][x]
        if i + 1 == len(exits):
            print(f'{x} ({room_id})', end='')
        else:
            print(f'{x} ({room_id})', end=', ')
    print(']')
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
    print()


def print_info(request):
    print(request)


def get_req(endpoint):
    req = get(end[endpoint])
    if endpoint == 'init':
        print_room(req)
    else:
        print_info(req)


def well():
    global data
    well = gr.get_path_to_room(data, 55)
    print_room(well)
    data = well
    return well


def travel(room_id):
    global data
    travelled = gr.get_path_to_room(data, int(room_id))
    print_room(travelled)
    data = travelled
    return travelled


def move(direction):
    global data
    room_in_dir = gr.rooms[data['room_id']]['exits'][direction]
    moved = post(end['move'], {'direction': direction,
                               'next_room_id': str(room_in_dir)})
    print_room(moved)
    data = moved
    return moved


def examine(target):
    examined = post(end['examine'], {'name': target})
    print_info(examined)
    if data['room_id'] == 55:
        ls8 = examined['description'][39:].split('\n')
        with open('ls8.ls8', 'w') as ls:
            ls.truncate()
            for line in ls8:
                if line != '':
                    json.dump(int(line), ls)
                    ls.write('\n')
        os.system('python ls8.py ls8.ls8')
    return examined


global cmds
cmds = {
    'mine': mine,
    'pray': pray,
    'well': well,
    'exits': exits,
    'self': {
        'bal': get_req,
        'status': get_req,
    },
    'double': {
        'travel': travel,
        'move': move,
        'examine': examine,
    }
}

instructions = f'''
Command options:
\tMine (begins mining for a coin)
\tPray (you pray in this room)
\tTravel <room> (begins a journey to <room> number)
\tExits (prints the exits in current room)
\tMove <direction> (will move you in the direction specified)
\tWell (begins a journey to the well)
\tBal (shows your current coin balance)
\tStatus (shows your character's status)
\tExamine <target> (examines the specified target - can be player or item)
\tRoom (shows details of current room)
\tTake <target> (picks up an item)
\tCarry <target> (TBD)
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
            print(f'Comman "{cmd}" not recognized.')

    elif command[0] in cmds['double']:
        cmds['double'][command[0]](command[1])

    else:
        print(f'Wtf is {cmd}?')
