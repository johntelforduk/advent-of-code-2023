# Advent of Code day 15, Lens Library.
# https://adventofcode.com/2023/day/15

from icecream import ic

def hash(s: str) -> int:
    current_value = 0

    for i in s:
        current_value += ord(i)
        current_value *= 17
        current_value = current_value % 256
    return current_value


with open('input.txt', 'r') as file:
    sequence = file.read()

ic(hash('HASH'))

total = 0
for step in sequence.split(','):
    total += hash(step)

ic(total)
