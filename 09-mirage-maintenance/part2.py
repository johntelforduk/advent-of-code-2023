# Advent of Code day 9, part 2, Mirage Maintenance.
# https://adventofcode.com/2023/day/9

from icecream import ic


def all_zeroes(num_list: list) -> bool:
    for i in num_list:
        if i != 0:
            return False
    return True


def calc_gaps(num_list: list) -> list:
    output = []
    previous = None
    for i in num_list:
        if previous is not None:
            output.append(i - previous)
        previous = i
    return output


assert all_zeroes([0]) is True
assert all_zeroes([0, 0, 0, 0]) is True
assert all_zeroes([0, 0, 0, 9]) is False
assert all_zeroes([9, 0, 0, 0]) is False

assert calc_gaps([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]
assert calc_gaps([1, 3, 6, 10, 15, 21]) == [2, 3, 4, 5, 6]

with open('input.txt', 'r') as file:
    report = file.read()

total = 0
for line in report.split('\n'):
    history = [int(value) for value in line.split()]

    rows = [history]
    while not all_zeroes(rows[-1]):          # Is the last row all zeroes?
        rows.append(calc_gaps(rows[-1]))

    rows.reverse()

    first_num = 0
    for row in rows:

        first_num = row[0] - first_num
        ic(row, first_num)
    ic(history, rows, first_num)
    total += first_num

ic(total)
