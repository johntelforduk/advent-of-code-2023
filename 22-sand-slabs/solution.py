# Advent of Code day 22, Sand Slabs.
# https://adventofcode.com/2023/day/22

from icecream import ic
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import random


def occupies(cuboid: tuple) -> set:
    x1, y1, z1, x2, y2, z2, _, _ = cuboid
    occ = set()
    for x in range(x1, x2):
        for y in range(y1, y2):
            for z in range(z1, z2):
                occ.add((x, y, z))
    return occ


def drop(cuboid: tuple, settled: set) -> tuple:
    x1, y1, z1, x2, y2, z2, colour, cube_no = cuboid
    if z1 == 1:
        return cuboid

    dz1, dz2 = z1, z2

    settled_try = settled.copy()
    none_lost = len(settled_try) + len(occupies(cuboid))

    while dz1 >= 1 and none_lost == len(settled_try.union(occupies((x1, y1, dz1, x2, y2, dz2, colour, cube_no)))):
        dz1 -= 1
        dz2 -= 1
    return x1, y1, dz1 + 1, x2, y2, dz2 + 1, colour, cube_no


def drop_the_cuboids(cuboids: list) -> list:
    dropped = []
    settled = set()

    for i in range(len(cuboids)):
        dropped_cuboid = drop(cuboids[i], settled)
        dropped.append(dropped_cuboid)
        settled = settled.union(occupies(dropped_cuboid))
    return dropped


def sort_cuboids(cuboids: list) -> list:
    cuboids_copy = cuboids.copy()
    sorted_cuboids = []
    while len(cuboids_copy) != 0:
        i = 0
        lowest = None
        pos = None
        for _, _, y, _, _, _, _, _ in cuboids_copy:
            if lowest is None:
                lowest = y
                pos = i
            elif y < lowest:
                lowest = y
                pos = i
            i += 1

        sorted_cuboids.append(cuboids_copy.pop(pos))
    return sorted_cuboids


def plot(cuboids: list):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    mx, my, mz = 0, 0, 0
    for _, _, _, x2, y2, z2, _, _ in cuboids:
        mx = max(mx, x2)
        my = max(my, y2)
        mz = max(mz, z2)

    ax.set_xlim(0, mx)
    ax.set_ylim(0, my)
    ax.set_zlim(0, mz)

    ax.set_aspect('equal')

    for c in cuboids:
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
                                             linewidths=0.2,
                                             edgecolors='black',
                                             alpha=1))

    ax.set_axis_off()
    plt.show()


with open('input.txt', 'r') as file:
    bricks_str = file.read()

random.seed(30)

cuboids = []
cuboid_no = 1
for line in bricks_str.split('\n'):
    origin, destination = line.split('~')
    xa, ya, za = [int(i) for i in origin.split(',')]
    xb, yb, zb = [int(i) for i in destination.split(',')]

    x1, x2 = min(xa, xb), max(xa, xb)
    y1, y2 = min(ya, yb), max(ya, yb)
    z1, z2 = min(za, zb), max(za, zb)
    colour = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    cuboids.append((x1, y1, z1, x2 + 1, y2 + 1, z2 + 1, colour, cuboid_no))
    cuboid_no += 1

cuboids = sort_cuboids(cuboids)
dropped = drop_the_cuboids(cuboids)

# Key = co-ordinates of a cube. Value = number of the cuboid that occupies it.
occupation = {}
for cuboid in dropped:
    _, _, _, _, _, _, _, cuboid_no = cuboid
    for (x, y, z) in occupies(cuboid):
        occupation[(x, y, z)] = cuboid_no

# Key = cuboid number. Value = set of cuboid numbers for cuboids that support it.
supported_by = {}
for cuboid in dropped:
    _, _, _, _, _, _, _, cuboid_no = cuboid
    for x, y, z in occupies(cuboid):
        if (x, y, z - 1) in occupation:
            if occupation[(x, y, z - 1)] != cuboid_no:
                if cuboid_no not in supported_by:
                    supported_by[cuboid_no] = set()
                supported_by[cuboid_no].add(occupation[(x, y, z - 1)])

singletons = set()
for cuboid in supported_by:
    if len(supported_by[cuboid]) == 1:
        singletons = singletons.union(supported_by[cuboid])

ic(len(dropped) - len(singletons))

plot(dropped)
