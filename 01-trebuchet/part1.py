# Advent of code day 1, Trebuchet?!
# https://adventofcode.com/2023/day/1

from icecream import ic

with open('input.txt', 'r') as file:
    document = file.read()

total = 0
for line in document.split('\n'):
    first_digit = None
    last_digit = None
    for this in line:
        if this.isdigit():
            value = int(this)
            if first_digit is None:
                first_digit = value
            last_digit = value
    ic(first_digit, last_digit)

    calibration = 10 * first_digit + last_digit
    total += calibration

print(total)
