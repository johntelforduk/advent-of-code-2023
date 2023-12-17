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

    def south(self):
        moving = True

        while moving:
            moving = False
            for y in reversed(range(self.height - 1)):
                for x in range(self.width):
                    if self.grid[(x, y + 1)] == '.' and self.grid[(x, y)] == 'O':
                        self.grid[(x, y + 1)] = 'O'
                        self.grid[(x, y)] = '.'
                        moving = True

    def west(self):
        moving = True

        while moving:
            moving = False
            for x in range(self.width - 1):
                for y in range(self.height):
                    if self.grid[(x, y)] == '.' and self.grid[(x + 1, y)] == 'O':
                        self.grid[(x, y)] = 'O'
                        self.grid[(x + 1, y)] = '.'
                        moving = True

    def east(self):
        moving = True

        while moving:
            moving = False
            for x in range(self.width - 1):
                for y in range(self.height):
                    if self.grid[(x + 1, y)] == '.' and self.grid[(x, y)] == 'O':
                        self.grid[(x + 1, y)] = 'O'
                        self.grid[(x, y)] = '.'
                        moving = True

    def calc_load(self) -> int:
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[(x, y)] == 'O':
                    total += self.height - y
        return total

    def cycle(self):
        self.north()
        self.west()
        self.south()
        self.east()

    def hash_grid(self):
        return hash(frozenset(self.grid.items()))


with open('input.txt', 'r') as file:
    positions = file.read()

my_dish = Dish(positions)

hash_history = {}
cycle_history = {}

cycles = 0
finished = False
while not finished:
    my_dish.cycle()
    cycles += 1
    ic(cycles, my_dish.calc_load())

    this_hash = my_dish.hash_grid()
    if this_hash in hash_history:
        finished = True
    else:
        hash_history[this_hash] = cycles

    cycle_history[cycles] = my_dish.calc_load()

ic(hash_history[this_hash])

cycle_length = cycles - hash_history[this_hash]
lead_in = cycles - cycle_length

ic(lead_in, cycle_length)

position = lead_in + ((1000000000 - lead_in) % cycle_length)
ic(position)
ic(cycle_history[position])
