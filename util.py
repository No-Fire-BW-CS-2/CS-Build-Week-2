from random import choice
import json
from urls import post, get, end


class Queue:
    def __init__(self):
        self.storage = []
        self.size = 0

    def enqueue(self, val):
        self.size += 1
        self.storage.append(val)

    def dequeue(self):
        if self.size:
            self.size -= 1
            return self.storage.pop(0)
        else:
            return None


class Stack:
    def __init__(self):
        self.storage = []
        self.size = 0

    def push(self, val):
        self.size += 1
        self.storage.append(val)

    def pop(self):
        if self.size:
            self.size -= 1
            return self.storage.pop()
        else:
            return None


reverse_dirs = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}


class Graph:

    """Represent the world as a dictionary of rooms mapping (room, dir) as edge."""

    def __init__(self):
        self.rooms = {}

    def add_vertex(self, room):
        """
        Add a vertex to the graph.
        """
        if room['room_id'] not in self.rooms:
            self.rooms[room['room_id']] = room
            self.rooms[room['room_id']]['exits'] = {d: '?' for d in room['exits']}
        

    def dfs(self, room):
        next_dirs = self.get_unexplored_dir(room)
        if len(next_dirs):
            direction = choice(next_dirs)
            next_room = self.explore(direction, room)
            return self.dfs(next_room)

    def get_unexplored_dir(self, room):
        return [direction for direction, value in self.rooms[room['room_id']]['exits'].items() if value == '?']

    def explore(self, direction, room):
        prev_room = room['room_id']
        res = post(end['move'], {'direction': direction})
        self.rooms[prev_room]['exits'][direction] = res['room_id']
        self.add_vertex(res)
        self.rooms[res['room_id']]['exits'][reverse_dirs[direction]] = prev_room
        print(self.rooms[prev_room])
        print(res)
        return res
