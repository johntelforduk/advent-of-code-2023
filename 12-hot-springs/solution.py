# Advent of Code day 12, Hot Springs.
# https://adventofcode.com/2023/day/12

from icecream import ic
import re
from itertools import product


with open('input.txt', 'r') as file:
    conditions = file.read()

zero_or_more_dots = "\\.*"
one_or_more_dots = "\\.+"

total_arrangements = 0

for line in conditions.split('\n'):
    condition_record, groups = line.split(' ')
    ic(line, condition_record, groups)

    pattern_regex = zero_or_more_dots
    for group_str in groups.split(','):
        if pattern_regex != zero_or_more_dots:
            pattern_regex += one_or_more_dots
        group = int(group_str)
        pattern_regex += "#" * group
    pattern_regex += zero_or_more_dots

    pattern = re.compile(pattern_regex)

    question_marks = []
    i = 0
    for each in condition_record:
        if each == "?":
            question_marks.append(i)
        i += 1

    for possible in product('.#', repeat=len(question_marks)):
        possible_list = list(possible)

        pos = 0
        for sub_pos in question_marks:
            condition_record = condition_record[:sub_pos] + possible_list[pos] + condition_record[sub_pos + 1:]
            pos += 1

        if pattern.fullmatch(condition_record):
            total_arrangements += 1

ic(total_arrangements)
