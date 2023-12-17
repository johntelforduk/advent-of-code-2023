# Advent of Code day 14, Parabolic Reflector Dish.
# https://adventofcode.com/2023/day/14

from icecream import ic

class Dish:

    def __init__(self, positions: str):
        self.grid = {}

        y = 0
        for row in positions.split('\n'):
            x = 0
            for item in row:
                self.grid[(x, y)] = item
                x += 1
            y += 1

        self.width, self.height = x, y

        ic(self.width, self.height)

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.grid[x, y], end='')
            print()

    def north(self):
        moving = True

        while moving:
            moving = False
            for y in range(self.height - 1):
                for x in range(self.width):
                    if self.grid[(x, y)] == '.' and self.grid[(x, y + 1)] == 'O':
                        self.grid[(x, y)] = 'O'
                        self.grid[(x, y + 1)] = '.'
                        moving = True

    def calc_load(self) -> int:
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[(x, y)] == 'O':
                    total += self.height - y
        return total


with open('input.txt', 'r') as file:
    positions = file.read()

my_dish = Dish(positions)
my_dish.render()
print()
my_dish.north()
my_dish.render()
ic(my_dish.calc_load())