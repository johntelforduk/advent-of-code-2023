# Advent of Code day 24, part 2, Never Tell Me The Odds.
# https://adventofcode.com/2023/day/24

from icecream import ic
import sympy

with open('input.txt', 'r') as file:
    hailstones_str = file.read()

hailstones = []

for line in hailstones_str.split('\n'):
    position_str, velocity_str = line.split(' @ ')
    px, py, pz = [int(i) for i in position_str.split(', ')]
    vx, vy, vz = [int(i) for i in velocity_str.split(', ')]

    hailstones.append((px, py, pz, vx, vy, vz))

ic(hailstones)

# Three 'times', as the rock will hit the hailstones at different times.
t1, t2, t3 = sympy.symbols('t1 t2 t3')

# 'r' is for 'Rock'.
pxr, vxr = sympy.symbols('pxr vxr')
pyr, vyr = sympy.symbols('pyr vyr')
pzr, vzr = sympy.symbols('pzr vzr')

# Starting coordinates and velocities of the 3 sample hailstones.
px1, py1, pz1, vx1, vy1, vz1 = hailstones[0]
px2, py2, pz2, vx2, vy2, vz2 = hailstones[1]
px3, py3, pz3, vx3, vy3, vz3 = hailstones[2]

# The 9 simultaneous equations.
x1 = sympy.Eq(pxr + t1 * vxr, px1 + vx1 * t1)
x2 = sympy.Eq(pxr + t2 * vxr, px2 + vx2 * t2)
x3 = sympy.Eq(pxr + t3 * vxr, px3 + vx3 * t3)
y1 = sympy.Eq(pyr + t1 * vyr, py1 + vy1 * t1)
y2 = sympy.Eq(pyr + t2 * vyr, py2 + vy2 * t2)
y3 = sympy.Eq(pyr + t3 * vyr, py3 + vy3 * t3)
z1 = sympy.Eq(pzr + t1 * vzr, pz1 + vz1 * t1)
z2 = sympy.Eq(pzr + t2 * vzr, pz2 + vz2 * t2)
z3 = sympy.Eq(pzr + t3 * vzr, pz3 + vz3 * t3)

# 's' is for 'Solution'.
pxs, pys, pzs, _, _, _, _, _, _ = sympy.solve([x1, x2, x3, y1, y2, y3, z1, z2, z3],
                                              (pxr, pyr, pzr, vxr, vyr, vzr, t1, t2, t3))[0]

ic(pxs, pys, pzs, pxs + pys + pzs)
