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

starting_position = get(end['init'])
gr = Graph()
gr.add_vertex(data)

status = post(end['status'], {})
gold = int(status['gold'])
encumbrance = int(status['encumbrance'])
strength = int(status['strength'])

while gold < 1000:
    while encumbrance < strength:
        dfs = gr.dfs(data)
        curr_room = gr.rooms[dfs[-1]]
        for room_id in dfs:
            visited.add(room_id)
        print('visited rooms ---->', visited)
        unexplored_dirs = gr.get_unexplored_dir(curr_room)
        data = curr_room
        if not len(unexplored_dirs):
            data = gr.backtrack_to_unex(curr_room)
        print("current room ---->", data)

while gold < 1000:
    while encumbrance < strength:
        gr.dfs(data)
        # traverse and pick up treasure until your overencumbered
        # navigate immediately to the store and sell your treasure
