# Advent of Code day 13, Point of Incidence.
# https://adventofcode.com/2023/day/13

from icecream import ic


with open('input.txt', 'r') as file:
    patterns = file.read()


def check_pair_of_rows(pattern: dict, y1: int, y2: int) -> bool:
    x = 1
    while (x, y1) in pattern or (x, y2) in pattern:
        if (x, y1) not in pattern or (x, y2) not in pattern:
            pass
        else:
            if pattern[(x, y1)] != pattern[(x, y2)]:
                return False
        x += 1
    return True


def check_row_reflection(pattern: dict, y: int) -> bool:
    # ic(check_pair_of_rows(pattern, 4, 5))
    # ic(check_pair_of_rows(pattern, 3, 6))
    # ic(check_pair_of_rows(pattern, 2, 7))
    # _, num_rows = max(pattern)
    # if y < 1 or y > num_rows:          # Top and bottom rows can't be place of reflection.
    #     return False

    y1, y2 = y, y + 1
    # _, height = max(pattern)
    while y1 >= 1:
        # ic(y1, y2)
        if check_pair_of_rows(pattern, y1, y2) is False:
            return False
        y1 -= 1
        y2 += 1
    return True
    # ic(max(pattern))


def row_reflection_score(pattern) -> int:
    _, num_rows = max(pattern)
    ic(num_rows)
    total = 0
    for check_y in range(1, num_rows):
        ic(check_y)
        if check_row_reflection(pattern, check_y):
            total += check_y
    return total


def rotate(pattern):
    new_pattern = {}
    width, height = max(pattern)
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            # ic(x, y)
            new_pattern[(height - y + 1, x)] = pattern[(x, y)]
    return new_pattern


total = 0
for pattern_str in patterns.split('\n\n'):
    pattern = {}
    y = 1
    for line in pattern_str.split('\n'):
        x = 1
        for each in line:
            pattern[(x, y)] = each
            x += 1
        y += 1

    # ic(min(pattern), max(pattern))
    total += 100 * row_reflection_score(pattern)

    rotated = rotate(pattern)
    # ic(rotated)

    # ic(min(rotated), max(rotated))
    total += row_reflection_score(rotated)

ic(row_reflection_score(pattern))


ic(total)
