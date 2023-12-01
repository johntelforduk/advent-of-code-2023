# Advent of code day 1, part 2, Trebuchet?!
# https://adventofcode.com/2023/day/1

from icecream import ic

with open('input.txt', 'r') as file:
    document = file.read()

word_to_digit = [('one', 1),
                 ('two', 2),
                 ('three', 3),
                 ('four', 4),
                 ('five', 5),
                 ('six', 6),
                 ('seven', 7),
                 ('eight', 8),
                 ('nine', 9)]
total = 0

for line in document.split('\n'):
    first_digit = None
    last_digit = None

    for pos in range(len(line)):
        value = None
        if line[pos].isdigit():
            value = int(line[pos])

        else:
            for word, digit in word_to_digit:
                if line[pos: (pos + len(word))] == word:
                    value = digit

        if value is not None:
            if first_digit is None:
                first_digit = value
            last_digit = value

    calibration = 10 * first_digit + last_digit
    ic(line, calibration)

    total += calibration

print(total)
