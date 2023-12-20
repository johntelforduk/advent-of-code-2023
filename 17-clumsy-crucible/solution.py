# Advent of Code day 17, Clumsy Crucible.
# https://adventofcode.com/2023/day/17

from icecream import ic
import sys

with open('input.txt', 'r') as file:
    map_str = file.read()

simple_grid = {}
y = 0
for line in map_str.split('\n'):
    x = 0
    for c in line:
        simple_grid[(x, y)] = int(c)
        x += 1
    y += 1
# ic(simple_grid)

grid = {}
mx, my = max(simple_grid)
for x, y in simple_grid:
    heat_loss = simple_grid[(x, y)]
    # if x != 0 and y != 0:                       # The origin is a special case.
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

        # Skip impossible previous directions to get to edge nodes in the grid.
        if not(
            x == 0 and dx == 1
            or y == 0 and dy == 1
            or x == mx and dx == -1
            or y == my and dy == -1
        ):
            for consecutive in range(3):
                grid[(x, y, dx, dy, consecutive)] = heat_loss
grid[(0, 0, 0, 0, 0)] = 0

# ic(grid)

# Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# function Dijkstra(Graph, source):
#
# create vertex set Q
q, dist, prev, small_q = {}, {}, {}, {}
# for each vertex v in Graph:
for v in grid:
    # dist[v] ← INFINITY
    dist[v] = sys.maxsize
    # prev[v] ← UNDEFINED

    # Tuple. (previous x, previous y), (delta x, delta y), consecutive in that direction).
    prev[v] = None
    # add v to Q
    q[v] = dist[v]
# dist[source] ← 0

source = (0, 0, 0, 0, 0)

dist[source] = 0

q[source] = 0
small_q[source] = 0



# # while Q is not empty:
while len(q) != 0:
    len_q = len(q)
    if len_q % 100 == 0:
        ic(len_q)

#     # u ← vertex in Q with min dist[u]
    if len(small_q) != 0:
        u = min(small_q, key=q.get)
    else:
        u = min(q, key=q.get)

#     # remove u from Q
    del q[u]
    if u in small_q:
        del small_q[u]
#
#     # for each neighbor v of u still in Q:
    x, y, tx, ty, consecutive = u
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if not (dx == -tx and dy == -ty):           # Check not reversing.
            if dx == tx and dy == ty:
                v = (x + dx, y + dy, dx, dy, consecutive + 1)
            else:
                v = (x + dx, y + dy, dx, dy, 0)

            if v in q:

    #             # print('v:', v)
    #
    #             # print(v)
    #             # alt ← dist[u] + length(u, v)
                alt = dist[u] + grid[v]
                # XXX All edges are length one in this graph!!!
                # alt = dist[u] + 1
    #
    #
    #             # if alt < dist[v]:
                if alt < dist[v]:
                    # dist[v] ← alt
                    dist[v] = alt
                    if v in q:
                        q[v] = alt
                        small_q[v] = alt
                    # prev[v] ← u

                    prev[v] = u
#
# # return dist[], prev[]
# checked += 1
# shortest = min(shortest, dist[target])
# print('Checked, len(sources), shortest:', checked, len(sources), shortest)
#
# print(shortest)

target = max(grid)
ic(target)
ic(dist[target])




ic(mx, my)
best = sys.maxsize
for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    for consecutive in range(3):
        if (mx, my, dx, dy, consecutive) in dist:
            best = min(best, dist[(mx, my, dx, dy, consecutive)])

# this = (12, 12, 0, 1, 2)
# while this in prev:
#     this = prev[this]
#     x, y, _, _, _ = this
#     ic(x, y)
ic(best)
