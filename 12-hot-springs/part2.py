# Advent of Code day 12, part 2, Hot Springs.
# https://adventofcode.com/2023/day/12

from icecream import ic
import functools

# From, https://medium.com/@nkhaja/memoization-and-decorators-with-python-32f607439f84
def memoize(func):
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func


@memoize
def solution(condition_records: list, groups: list, banked_springs: int) -> int:

    # Success!
    if len(condition_records) == 0 and len(groups) == 0 and banked_springs == 0:
        return 1

    # Basic failure.
    if len(condition_records) == 0:
        return 0

    new_condition_records = condition_records.copy()
    front_condition = new_condition_records.pop(0)

    if front_condition == '#':
        return solution(new_condition_records, groups, banked_springs + 1)

    if front_condition == '.':
        if banked_springs == 0:         # One of a line of consecutive dots, so skip.
            return solution(new_condition_records, groups, banked_springs)

        if len(groups) == 0:
            return 0

        new_groups = groups.copy()
        front_group = new_groups.pop(0)

        # Failure: the group we are about to close has incorrect number of springs in it.
        if banked_springs != front_group:
            return 0

        return solution(new_condition_records, new_groups, 0)   # Start a new group.

    else:                           # Must be a question mark.
        new_condition_records2 = new_condition_records.copy()

        new_condition_records.insert(0, '.')
        new_condition_records2.insert(0, '#')

        return (solution(new_condition_records, groups, banked_springs)
                + solution(new_condition_records2, groups, banked_springs))


def process(line: str) -> int:
    condition_records_str, groups_str = line.split(' ')

    condition_record = [each for each in condition_records_str]
    groups = [int(group) for group in groups_str.split(',')]

    unfolded_condition_record = []
    for i in range(4):
        unfolded_condition_record += condition_record
        unfolded_condition_record.append('?')
    unfolded_condition_record += condition_record
    unfolded_condition_record.append('.')

    unfolded_groups = groups * 5
    return solution(unfolded_condition_record, unfolded_groups, 0)


with open('input.txt', 'r') as file:
    conditions = file.read()

total, line_no = 0, 0
for line in conditions.split('\n'):
    line_no += 1

    arrangements = process(line)
    ic(line_no, line, arrangements)
    total += arrangements

ic(total)
