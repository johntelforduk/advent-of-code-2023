# Advent of Code day 11, Cosmic Expansion.
# https://adventofcode.com/2023/day/11

from icecream import ic
from itertools import combinations


class Observatory:

    def __init__(self, s: str, age: int):
        self.galaxies = set()

        x, y = 0, 0
        for row in s.split('\n'):
            for c in row:
                if c == '#':
                    self.galaxies.add((x, y))
                x += 1
            self.width = x
            x = 0
            y += 1

        self.height = y

        self.horizontal_expansion = {}
        self.vertical_expansion = {}

        for y in range(self.height):
            no_galaxies = True
            for x in range(self.width):
                if (x, y) in self.galaxies:
                    no_galaxies = False
            if no_galaxies:
                self.vertical_expansion[y] = age - 1

        for x in range(self.width):
            no_galaxies = True
            for y in range(self.height):
                if (x, y) in self.galaxies:
                    no_galaxies = False
            if no_galaxies:
                self.horizontal_expansion[x] = age - 1

        ic(self.galaxies, self.width, self.height, self.vertical_expansion, self.horizontal_expansion)

    def manhattan(self, x1, y1, x2, y2) -> int:
        pre_expansion = abs(x1 - x2) + abs(y1 - y2)

        horizontal_add_on = 0
        fx, tx = min(x1, x2), max(x1, x2)
        for x in range(fx, tx):
            if x in self.horizontal_expansion:
                horizontal_add_on += self.horizontal_expansion[x]

        vertical_add_on = 0
        fy, ty = min(y1, y2), max(y1, y2)
        for y in range(fy, ty):
            if y in self.vertical_expansion:
                vertical_add_on += self.vertical_expansion[y]

        return pre_expansion + horizontal_add_on + vertical_add_on


with open('input.txt', 'r') as file:
    image_str = file.read()

my_observatory = Observatory(image_str, 1000000)
# assert (my_observatory.manhattan(1, 5, 4, 9)) == 9
# assert (my_observatory.manhattan(3, 0, 7, 8)) == 15

total = 0
for f, t in combinations(my_observatory.galaxies, 2):
    x1, y1 = f
    x2, y2 = t
    total += my_observatory.manhattan(x1, y1, x2, y2)

ic(total)
