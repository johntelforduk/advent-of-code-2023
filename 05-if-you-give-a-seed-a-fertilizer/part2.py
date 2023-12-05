# Advent of code day 5, part 2. If You Give A Seed A Fertilizer.
# https://adventofcode.com/2023/day/5

from icecream import ic


def parse_seeds(a: str) -> list:
    simple_list = [int(seed) for seed in a.replace('seeds:', '').split()]

    # Each item in list is a tuple. (start, length)
    seeds= []

    start = None
    while len(simple_list) != 0:
        next = simple_list.pop(0)
        if start is None:
            start = next
        else:
            seeds.append((start, next))
            start = None

    return seeds

def parse_map(a: str) -> tuple:
    terms = a.split('-')
    return terms[0], terms[2].replace(' map:', '')


def parse_range(a: str) -> list:
    return [int(term) for term in a.split(' ')]


def correspond(source: int, mappings: list) -> int:
    for destination_range_start, source_range_start, range_length in mappings:
        # 50, 98, 2
        # 98 + 2 = 100
        if source >= source_range_start and source < source_range_start + range_length:
            return destination_range_start - source_range_start + source
    return source


def seed_exists(candidate_seed: int, seeds: list) -> bool:
    for start, length in seeds:
        if start <= candidate_seed < start + length:
            return True
    return False


def back_correspond(target: int, mappings: list) -> int:
    for destination_range_start, source_range_start, range_length in mappings:
        backwards = source_range_start + target - destination_range_start
        if backwards >= source_range_start and backwards < source_range_start + range_length:
            return backwards
    return target


with open('input.txt', 'r') as file:
    almanac_str = file.read()

map_from, map_to, destination_range_start, source_range_start, range_length = None, None, None, None, None
mappings = []

# Key = tuple (map_from, map_to)
# Value = list of mappings. Each mappings is tuple (destination_range_start, source_range_start, range_length)
almanac = {}

# Key = destination, eg. "soil".
# Value = source, eg, "seed".
destination_to_source = {}

for line in almanac_str.split('\n'):
    if 'seeds:' in line:
        seeds = parse_seeds(line)

    elif len(line) != 0:            # Skip blank lines.
        # ic(line)

        if "map:" in line:
            if len(mappings) != 0:
                almanac[(map_from, map_to)] = mappings

            map_from, map_to = parse_map(line)
            destination_to_source[map_to] = map_from
            mappings = []

        else:
            destination_range_start, source_range_start, range_length = parse_range(line)
            mappings.append((destination_range_start, source_range_start, range_length))

        # ic(map_from, map_to, mappings)

almanac[(map_from, map_to)] = mappings

ic(seeds, almanac, destination_to_source)

start_target = 1
done = False

while not done:
    target = start_target
    map_to = 'location'
    map_from = destination_to_source[map_to]

    failure = False
    while not failure and map_to != 'seed':
        target = back_correspond(target=target, mappings=almanac[(map_from, map_to)])

        if target < 0:
            failure = True
        else:
            map_to = map_from
            if map_to in destination_to_source:
                map_from = destination_to_source[map_to]

    if not failure:
        if seed_exists(candidate_seed=target, seeds=seeds):
            done = True

    if not done:
        start_target += 1

    if start_target % 1000000 == 0:
        ic(start_target)

ic(failure, start_target)
