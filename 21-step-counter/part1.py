# Advent of Code day 21, Step Counter.
# https://adventofcode.com/2023/day/21

from icecream import ic

with open('input.txt', 'r') as file:
    map_str = file.read()

garden = {}
reachable = set()
steps = 0

y = 0
for line in map_str.split('\n'):
    x = 0
    for c in line:
        if c == 'S':
            garden[(x, y)] = '.'
            reachable.add((x, y))
        else:
            garden[(x, y)] = c
        x += 1
    y += 1

# ic(garden, reachable)

for steps in range(64):
    new_reachable = set()
    for x, y in reachable:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try_x, try_y = x + dx, y + dy
            if (try_x, try_y) in garden:
                if garden[(try_x, try_y)] == '.':
                    new_reachable.add((try_x, try_y))
    reachable = new_reachable
    ic(steps, len(reachable))

# ic(len(reachable))
