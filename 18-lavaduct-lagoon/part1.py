# Advent of Code day 18, Lavaduct Lagoon.
# https://adventofcode.com/2023/day/18

from icecream import ic

with open('input.txt', 'r') as file:
    dig_plan_str = file.read()


# def render(grid: dict):
#     for y in range(0, 62):
#         for x in range(150, 201):
#             if (x, y) in grid:
#                 print('#', end='')
#             else:
#                 print('.', end='')
#         print()


def flood_fill(x, y, grid):
    to_do = [(x, y)]

    while len(to_do) != 0:
        x, y = to_do.pop()

        if len(grid) % 1000 == 0:
            ic(len(to_do), len(grid), x, y)

        grid[(x, y)] = 'ffffff'
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            test_x, test_y = x + dx, y + dy

            if (test_x, test_y) not in grid and (test_x, test_y) not in to_do:
                to_do.append((test_x, test_y))


deltas = {'R': (1, 0), 'L': (-1, 0), 'D': (0, 1), 'U': (0, -1)}
grid = {}
x, y = 0, 0
lx, ly, hx, hy = 0, 0, 0, 0

for line in dig_plan_str.split('\n'):
    direction, distance_str, rgb = line.split(' ')
    distance = int(distance_str)

    dx, dy = deltas[direction]

    if (x, y) == (0, 0):
        grid[(x, y)] = rgb

    dx, dy = deltas[direction]
    for i in range(distance):
        x += dx
        y += dy
        grid[(x, y)] = rgb

flood_fill(0, 0, grid)
ic(len(grid))
