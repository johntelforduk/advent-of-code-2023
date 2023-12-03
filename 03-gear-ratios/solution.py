# Advent of code day 3, Gear Ratios.
# https://adventofcode.com/2023/day/3

from icecream import ic


def is_symbol(candidate: str) -> bool:
    return not(candidate == '.' or candidate.isdigit())


with open('input.txt', 'r') as file:
    games = file.read()

schematic = ['.' + line + '.' for line in games.split('\n')]
extra_row = '.' * len(schematic[0])
schematic.insert(0, extra_row)
schematic.append(extra_row)
ic(schematic)

this_number, number_sum = 0, 0

# Key = Co-ordinates of a gear, eg. (3, 1).
# Value = list of numbers adjacent to that gear, eg [467, 35].
gears = {}

for y in range(len(schematic)):
    for x in range(len(schematic[y])):
        if schematic[y][x].isdigit():
            this_number = 10 * this_number + int(schematic[y][x])
        elif this_number != 0:
            ic(this_number)

            # Search around the number.
            symbol_found = False
            for sy in range(y - 1, y + 2):
                for sx in range(x - len(str(this_number)) - 1, x + 1):
                    symbol_found = symbol_found or is_symbol(schematic[sy][sx])
                    ic(this_number, sx, sy, symbol_found)

                    # Check for gear.
                    if schematic[sy][sx] == '*':
                        if (sx, sy) in gears:
                            gears[(sx, sy)].append(this_number)
                        else:
                            gears[(sx, sy)] = [this_number]
                        ic(gears)

            if symbol_found:
                number_sum += this_number
            this_number = 0

# Add up the gear ratios.
ratio_sum = 0
for gear in gears:
    if len(gears[gear]) == 2:
        ratio_sum += gears[gear][0] * gears[gear][1]

ic(number_sum, ratio_sum)
