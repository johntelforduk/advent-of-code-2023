# Advent of Code day 18, part 2, Lavaduct Lagoon.
# https://adventofcode.com/2023/day/18

from icecream import ic

with open('input.txt', 'r') as file:
    dig_plan_str = file.read()

# 0 means R, 1 means D, 2 means L, and 3 means U.
deltas = {'0': (1, 0), '2': (-1, 0), '1': (0, 1), '3': (0, -1)}

vertices = []
x, y = 0, 0

vertices.append((x, y))

for line in dig_plan_str.split('\n'):
    _, _, hex_str = line.split(' ')

    distance = int(hex_str[2:7], 16)
    dx, dy = deltas[hex_str[7]]

    x, y = x + dx * distance, y + dy * distance
    vertices.append((x, y))

    ic(hex_str, distance, dx, dy)

ic(vertices)

# Algorithm from here, https://en.wikipedia.org/wiki/Shoelace_formula
a = 0
for i in range(len(vertices) - 1):
    xa, ya = vertices[i]
    xb, yb = vertices[i + 1]

    a += xa * yb - ya * xb + abs(xb - xa + yb - ya)

ic(1 + a // 2)
