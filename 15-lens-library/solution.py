# Advent of Code day 15, Lens Library.
# https://adventofcode.com/2023/day/15

from icecream import ic


def custom_hash(s: str) -> int:
    current_value = 0

    for i in s:
        current_value += ord(i)
        current_value *= 17
        current_value = current_value % 256
    return current_value


def find_label(search_list: list, search_label: str) -> int:
    pos = 0
    for label, _ in search_list:
        if label == search_label:
            return pos
        pos += 1
    return None


def focusing_power(hashmap: dict) -> int:
    total = 0
    for box in hashmap:
        slot_value = 1
        for _, focal_length in hashmap[box]:
            total += (box + 1) * slot_value * focal_length
            slot_value += 1
    return total


with open('input.txt', 'r') as file:
    sequence = file.read()

ic(custom_hash('HASH'))

total = 0

# Key = hashcode.
# Value = list of tuples. Each tuple is (label, focal length).
hashmap = {}

for step in sequence.split(','):
    total += custom_hash(step)

    if '=' in step:
        label = step.split('=')[0]
        focal_length = int(step.split('=')[1])
        operation = '='
    else:
        label = step.split('-')[0]
        operation = '-'

    box = custom_hash(label)

    if operation == '=':
        if box not in hashmap:
            hashmap[box] = [(label, focal_length)]
        else:
            position = find_label(search_list=hashmap[box], search_label=label)
            if position is None:
                hashmap[box].append((label, focal_length))
            else:
                hashmap[box][position] = (label, focal_length)

    else:                                   # Must be a "-" operation.
        if box in hashmap:
            position = find_label(search_list=hashmap[box], search_label=label)
            if position is not None:
                del hashmap[box][position]

ic(total)
ic(focusing_power(hashmap))
