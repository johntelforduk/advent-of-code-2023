# Advent of code day 8, part 2. Haunted Wasteland.
# https://adventofcode.com/2023/day/8

from icecream import ic
from math import gcd


class Ghost:

    def __init__(self, location: str, instructions: str, network: dict):
        self.location = location
        self.instructions = instructions
        self.network = network

        self.length = len(instructions)
        self.pos = 0
        self.steps = 0

    def reached_end(self) -> bool:
        return self.location[-1] == 'Z'

    def move(self):
        if self.instructions[self.pos] == 'L':
            self.location, _ = self.network[self.location]
        else:
            _, self.location = network[self.location]

        self.pos = (self.pos + 1) % self.length
        self.steps += 1


with open('input.txt', 'r') as file:
    map_txt = file.read()

instructions, network_str = map_txt.split('\n\n')

network = {}
for line in network_str.split('\n'):
    source, target_str = line.split(' = ')

    left, right = target_str.replace('(', '').replace(')', '').split(', ')
    network[source] = (left, right)

cycles = []
for source in network:
    if source[-1] == 'A':
        ghost = Ghost(location=source, instructions=instructions, network=network)

        while not ghost.reached_end():
            ghost.move()
        cycles.append(ghost.steps)

ic(cycles)

lcm = 1
for i in cycles:
    lcm = lcm * i // gcd(lcm, i)
ic(lcm)
