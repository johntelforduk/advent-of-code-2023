# Advent of Code day 16, The Floor Will Be Lava.
# https://adventofcode.com/2023/day/16

from icecream import ic


class Beam:

    def __init__(self, layout: dict, x:int, y:int, direction: str):
        self.layout = layout
        self.x = x
        self.y = y
        self.direction = direction

        self.max_x, self.max_y = max(self.layout)


    def move(self) -> str:
        deltas = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
        dx, dy = deltas[self.direction]
        self.x += dx
        self.y += dy

        # Beam has left the contraption.
        if self.x < 0 or self.x > self.max_x or self.y < 0 or self.y > self.max_y:
            return ''

        tile = self.layout[(self.x, self.y)]

        if tile == '\\':
            new_direction = {'R': 'D', 'U': 'L', 'L': 'U', 'D': 'R'}
            self.direction = new_direction[self.direction]
            return ''

        if tile == '/':
            new_direction = {'R': 'U', 'U': 'R', 'L': 'D', 'D': 'L'}
            self.direction = new_direction[self.direction]
            return ''

        if tile == '|':
            if self.direction in 'LR':
                self.direction = 'D'
                return 'U'

        if tile == '-':
            if self.direction in 'UD':
                self.direction = 'R'
                return 'L'

        return ''


def render(beam: Beam, energised: set):
    for y in range(beam.max_x + 1):
        for x in range(beam.max_y + 1):
            if (x, y) in energised:
                print('#', end='')
            else:
                print('.', end='')
        print()


def test_configuration(layout: dict, x: int, y: int, direction: str):
    first_beam = Beam(layout=layout, x=x, y=y, direction=direction)
    first_beam.move()
    beams = [first_beam]
    energised_direction = set()
    energised = set()

    while len(beams) > 0:
        this_beam = beams.pop(0)

        while ((this_beam.x, this_beam.y, this_beam.direction) not in energised_direction
               and 0 <= this_beam.x <= this_beam.max_x
               and 0 <= this_beam.y <= this_beam.max_y):
            energised_direction.add((this_beam.x, this_beam.y, this_beam.direction))
            energised.add((this_beam.x, this_beam.y))
            new_direction = this_beam.move()

            if new_direction != '':
                beams.append(Beam(layout=layout, x=this_beam.x, y=this_beam.y, direction=new_direction))

    beam = Beam(layout=layout, x=3, y=-1, direction='D')
    # render(beam, energised)
    return len(energised)


with open('input.txt', 'r') as file:
    contraption = file.read()

# Key = (x, y).
layout = {}

y = 0
for line in contraption.split('\n'):
    x = 0
    for c in line:
        layout[(x, y)] = c
        x += 1
    y += 1

ic(test_configuration(layout=layout, x=-1, y=0, direction='R'))

mx, my = max(layout)
assert mx == my
best = 0

for i in range(mx + 1):
    best = max(best, test_configuration(layout=layout, x=-1, y=i, direction='R'))
    best = max(best, test_configuration(layout=layout, x=i, y=-1, direction='D'))
    best = max(best, test_configuration(layout=layout, x=mx + 1, y=i, direction='L'))
    best = max(best, test_configuration(layout=layout, x=i, y=my + 1, direction='U'))

ic(best)
