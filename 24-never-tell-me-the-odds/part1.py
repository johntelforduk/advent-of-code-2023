# Advent of Code day 24, Never Tell Me The Odds.
# https://adventofcode.com/2023/day/24

from icecream import ic
import itertools

with open('input.txt', 'r') as file:
    hailstones_str = file.read()

lower, upper = 200000000000000, 400000000000000

hailstones = []

for line in hailstones_str.split('\n'):
    position_str, velocity_str = line.split(' @ ')
    px, py, pz = [int(i) for i in position_str.split(', ')]
    vx, vy, vz = [int(i) for i in velocity_str.split(', ')]

    # y = mx + c
    px2, py2 = px + vx, py + vy
    m = (py2 - py) / (px2 - px)
    c = py - m * px

    hailstones.append((px, py, pz, vx, vy, vz, m, c))

ic(hailstones)

count = 0
for a, b in itertools.combinations(hailstones, 2):
    x1, y1, _, vx1, vy1, _, m1, c1 = a
    x2, y2, _, vx2, vy2, _, m2, c2 = b

    if m1 == m2 and c1 != c2:           # Parallel lines.
        pass

    else:
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1

        if lower <= x <= upper and lower <= y <= upper:
            a_x_direction = ((x - x1) * vx1) > 0
            a_y_direction = ((y - y1) * vy1) > 0
            b_x_direction = ((x - x2) * vx2) > 0
            b_y_direction = ((y - y2) * vy2) > 0

            if a_x_direction and a_y_direction and b_x_direction and b_y_direction:
                # ic(a, b, x, y, a_x_direction, a_y_direction, b_x_direction, b_y_direction)
                count += 1

ic(count)
