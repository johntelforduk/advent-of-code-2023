# Advent of Code day 22, Sand Slabs.
# https://adventofcode.com/2023/day/22

from icecream import ic
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import random


def occupies(cube: tuple) -> set:
    x1, y1, z1, x2, y2, z2, _, _ = cube
    occ = set()
    for x in range(x1, x2):
        for y in range(y1, y2):
            for z in range(z1, z2):
                occ.add((x, y, z))
    return occ


def drop(cube: tuple, settled: set) -> tuple:
    x1, y1, z1, x2, y2, z2, colour, cube_pos = cube
    if z1 == 1:
        return cube

    dz1, dz2 = z1, z2

    settled_try = settled.copy()
    none_lost = len(settled_try) + len(occupies(cube))

    while dz1 >= 0 and none_lost == len(settled_try.union(occupies((x1, y1, dz1, x2, y2, dz2, colour, cube_pos)))):
        dz1 -= 1
        dz2 -= 1
        # settled_try = settled.copy()
        # settled_try = settled_try.union(occupies((x1, y1, dz1, x2, y2, dz2, colour)))
    return x1, y1, dz1 + 1, x2, y2, dz2 + 1, colour, cube_pos


def sort_cubes(cubes_copy: list) -> list:
    cubes_copy = cubes.copy()
    sorted_cubes = []
    while len(cubes_copy) != 0:
        i = 0
        lowest = None
        pos = None
        for _, _, y, _, _, _, _, _ in cubes_copy:
            if lowest is None:
                lowest = y
                pos = i
            elif y < lowest:
                lowest = y
                pos = i
            i += 1

        sorted_cubes.append(cubes_copy.pop(pos))
    return sorted_cubes


# def int_to_zero_one(i: int) -> float:
#     return float('0.' + str(i))


# def pick_colour(cube: tuple) -> tuple:
#     x1, y1, z1, x2, y2, z2 = cube
#     seed = 147
#     hash = 1
#     pos = 1
#     for i in [x1, y1, z1, x2, y2, z2]:
#         hash *= (i + 1) * seed
#         seed *= 147
#
#     h2 = hash * 147
#     h3 = h2 * 147
#     # ic(hash, h2, h3)
#
#     return int_to_zero_one(hash), int_to_zero_one(h2), int_to_zero_one(h3)


def plot(cubes: list, mx, my, mz):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(0, mx)
    ax.set_ylim(0, my)
    ax.set_zlim(0, mz)

    ax.set_aspect('equal')

    for c in cubes:
        x1, y1, z1, x2, y2, z2, colour, _ = c
        v = np.array([[x1, y1, z1], [x2, y1, z1], [x2, y2, z1], [x1, y2, z1],
                      [x1, y1, z2], [x2, y1, z2], [x2, y2, z2], [x1, y2, z2]])

        ax.scatter3D(v[:, 0], v[:, 0], v[:, 0], s=0)  # Needed to set the bounds of the plotting space.

        faces = [[v[0], v[1], v[2], v[3]],
                 [v[4], v[5], v[6], v[7]],
                 [v[1], v[5], v[6], v[2]],
                 [v[0], v[4], v[7], v[3]],
                 [v[3], v[2], v[6], v[7]],
                 [v[0], v[1], v[5], v[4]]]

        # Plot faces.
        ax.add_collection3d(Poly3DCollection(faces,
                                             facecolors=colour,
                                             linewidths=0.1,
                                             edgecolors='black',
                                             alpha=1))

    ax.set_axis_off()
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    plt.show()


with open('test.txt', 'r') as file:
    bricks_str = file.read()

random.seed(30)

cubes = []
cube_no = 1
for line in bricks_str.split('\n'):
    origin, destination = line.split('~')
    xa, ya, za = [int(i) for i in origin.split(',')]
    xb, yb, zb = [int(i) for i in destination.split(',')]

    x1, x2 = min(xa, xb), max(xa, xb)
    y1, y2 = min(ya, yb), max(ya, yb)
    z1, z2 = min(za, zb), max(za, zb)
    colour = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    cubes.append((x1, y1, z1, x2 + 1, y2 + 1, z2 + 1, colour, cube_no))
    cube_no += 1

cubes = sort_cubes(cubes)
ic(cubes)

min_x, max_x, min_y, max_y, min_z, max_z = 100000, -100000, 100000, -100000, 100000, -100000
for x1, y1, z1, x2, y2, z2, _, _ in cubes:
    min_x = min(min_x, x1)
    min_y = min(min_y, y1)
    min_z = min(min_z, z1)
    max_x = max(max_x, x2)
    max_y = max(max_y, y2)
    max_z = max(max_z, z2)

ic(min_x, max_x, min_y, max_y, min_z, max_z)

ic(occupies(cubes[0]))

dropped = []
settled = set()

for i in range(len(cubes)):
    dropped_cube = drop(cubes[i], settled)
    dropped.append(dropped_cube)
    settled = settled.union(occupies(dropped_cube))

plot(dropped, max_x, max_y, max_z)
