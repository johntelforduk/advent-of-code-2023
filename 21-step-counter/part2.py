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
mx, my = max(garden)
ic(mx, my)

# def count_in_zone(x1, x2, y1, y2, reachable):
#     count = 0
#     for x in range(x1, x2 + 1):
#         for y in range(y1, y2 + 1):
#             if (x, y) in reachable:
#                 count += 1
#     return count


target = 26501365
offset = ic(target % 131)

steps = 0
while steps < offset + 1 + 2 * 131:
    steps += 1
    new_reachable = set()
    for x, y in reachable:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try_x, try_y = x + dx, y + dy
            map_x = try_x % (mx + 1)
            map_y = try_y % (my + 1)

            if garden[(map_x, map_y)] == '.':
                new_reachable.add((try_x, try_y))
    reachable = new_reachable
    if (steps - offset) % 131 == 0:
        print(f'{steps}, {len(reachable)}')

# These 3 solutions are produced,
# (65, 3755)
# (196, 33494)
# (327, 92811)
#
# Then, asked WoolframAlpha to work out the terms in the quadratic that fits these points,
# https://www.wolframalpha.com/input?i=quadratic+%2865%2C3755%29+%28196%2C33494%29+%28327%2C92811%29
#
# Finally, put these terms into formula.

ic((target * target * 14789 + target * 35880 - 376170) / 17161)
