# Advent of code day 8, Haunted Wasteland
# https://adventofcode.com/2023/day/8

from icecream import ic


class Instructions:

    def __init__(self, instructions:str):
        self.instructions = instructions
        self.length = len(instructions)
        self.pos = 0

    def next(self) -> str:
        move = self.instructions[self.pos]
        self.pos = (self.pos + 1) % self.length
        return move


test_inst = Instructions('LRR')
assert test_inst.next() == 'L'
assert test_inst.next() == 'R'
assert test_inst.next() == 'R'
assert test_inst.next() == 'L'
assert test_inst.next() == 'R'

with open('input.txt', 'r') as file:
    map_txt = file.read()

instructions, network_str = map_txt.split('\n\n')

ic(instructions, network_str)

network = {}
for line in network_str.split('\n'):
    source, target_str = line.split(' = ')

    left, right = target_str.replace('(', '').replace(')', '').split(', ')
    network[source] = (left, right)
    ic(source, target_str, left, right)

ic(network)

my_instructions = Instructions(instructions)
steps = 0
source = 'AAA'
while source != 'ZZZ':
    next_step = my_instructions.next()

    if next_step == 'L':
        source, _ = network[source]
    else:
        _, source = network[source]

    steps += 1

ic(steps)
