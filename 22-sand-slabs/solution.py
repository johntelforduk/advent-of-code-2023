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

    while dz1 >= 1 and none_lost == len(settled_try.union(occupies((x1, y1, dz1, x2, y2, dz2, colour, cube_pos)))):
        dz1 -= 1
        dz2 -= 1
        # settled_try = settled.copy()
        # settled_try = settled_try.union(occupies((x1, y1, dz1, x2, y2, dz2, colour)))
    return x1, y1, dz1 + 1, x2, y2, dz2 + 1, colour, cube_pos


def drop_the_cuboids(cubes: list) -> list:
    dropped = []
    settled = set()

    for i in range(len(cubes)):
        dropped_cube = drop(cubes[i], settled)
        dropped.append(dropped_cube)
        settled = settled.union(occupies(dropped_cube))
    return dropped


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
                                             linewidths=0.2,
                                             edgecolors='black',
                                             alpha=1))

    ax.set_axis_off()
    plt.show()


with open('input.txt', 'r') as file:
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

c1 = 0
for c in cubes:
    c1 += len(occupies(c))
ic(c1)


cubes = sort_cubes(cubes)
c2 = 0
for c in cubes:
    c2 += len(occupies(c))
ic(c2)

# for _, _, z, _, _, _, _, _ in cubes:
#     ic(z)


# ic(cubes)

min_x, max_x, min_y, max_y, min_z, max_z = 100000, -100000, 100000, -100000, 100000, -100000
for x1, y1, z1, x2, y2, z2, _, _ in cubes:
    min_x = min(min_x, x1)
    min_y = min(min_y, y1)
    min_z = min(min_z, z1)
    max_x = max(max_x, x2)
    max_y = max(max_y, y2)
    max_z = max(max_z, z2)

# ic(min_x, max_x, min_y, max_y, min_z, max_z)

# ic(occupies(cubes[0]))

# settled = set()

dropped = drop_the_cuboids(cubes)

c3 = 0
for c in dropped:
    c3 += len(occupies(c))
ic(c3)



# Key = co-ordinates of a cube. Value = number of the cuboid that occupies it.
occupation = {}
for cuboid in dropped:
    _, _, _, _, _, _, _, cube_pos = cuboid
    for (x, y, z) in occupies(cuboid):
        occupation[(x, y, z)] = cube_pos
# ic(occupation)

# Key = cuboid number. Value = set of cuboid numbers for cuboids that support it.
supported_by = {}
for cuboid in dropped:
    _, _, _, _, _, _, _, cube_no = cuboid
    for x, y, z in occupies(cuboid):
        if (x, y, z - 1) in occupation:
            if occupation[(x, y, z - 1)] != cube_no:
                if cube_no not in supported_by:
                    supported_by[cube_no] = set()
                supported_by[cube_no].add(occupation[(x, y, z - 1)])


ic(supported_by)

singletons = set()
for cuboid in supported_by:
    if len(supported_by[cuboid]) == 1:
        singletons = singletons.union(supported_by[cuboid])

ic(singletons)
ic(len(dropped) - len(singletons))

plot(dropped, max_x, max_y, max_z)