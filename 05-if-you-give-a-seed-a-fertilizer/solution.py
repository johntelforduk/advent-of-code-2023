# Advent of code day 5, If You Give A Seed A Fertilizer..
# https://adventofcode.com/2023/day/5

from icecream import ic


def parse_seeds(a: str) -> list:
    return [int(seed) for seed in a.replace('seeds:', '').split()]


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


with open('input.txt', 'r') as file:
    almanac_str = file.read()

map_from, map_to, destination_range_start, source_range_start, range_length = None, None, None, None, None
mappings = []

# Key = tuple (map_from, map_to)
# Value = list of mappings. Each mappings is tuple (destination_range_start, source_range_start, range_length)
almanac = {}

# Key = source, eg. "seed".
# Value = destination, eg, "soil".
source_to_destination = {}

for line in almanac_str.split('\n'):
    if 'seeds:' in line:
        seeds = parse_seeds(line)

    elif len(line) != 0:            # Skip blank lines.
        ic(line)

        if "map:" in line:
            if len(mappings) != 0:
                almanac[(map_from, map_to)] = mappings

            map_from, map_to = parse_map(line)
            source_to_destination[map_from] = map_to
            mappings = []

        else:
            destination_range_start, source_range_start, range_length = parse_range(line)
            mappings.append((destination_range_start, source_range_start, range_length))

        ic(map_from, map_to, mappings)

almanac[(map_from, map_to)] = mappings

ic(seeds, almanac, source_to_destination)

# for test in range(110):
#     correspondence = correspond(source=test, mappings=almanac[("seed", "soil")])
#     ic(test, correspondence)
best = None

for source in seeds:
    map_from = 'seed'
    map_to = source_to_destination[map_from]

    while map_from != 'location':
        source = correspond(source=source, mappings=almanac[(map_from, map_to)])

        map_from = map_to
        if map_from in source_to_destination:
            map_to = source_to_destination[map_from]

    if best is None:
        best = source
    else:
        best = min(best, source)

ic(best)
