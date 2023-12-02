# Advent of code day 2, Cube Conundrum.
# https://adventofcode.com/2023/day/2

from icecream import ic

with open('input.txt', 'r') as file:
    games = file.read()

capacity = {'red': 12, 'green': 13, 'blue': 14}
id_total, power_sum = 0, 0

for game in games.split('\n'):
    gn_part, gp_part = game.split(': ')
    game_no = int(gn_part.split(' ')[1])
    ic(gn_part, gp_part, game_no)

    possible = True
    power_terms = {'red': 1, 'green': 1, 'blue': 1}
    for handful in gp_part.split('; '):
        handful_dict = {}
        cubes = 0
        for element in handful.replace(',', '').split(' '):
            if element.isnumeric():
                cubes = int(element)
            else:
                handful_dict[element] = cubes
        ic(capacity, handful, handful_dict)

        for colour in handful_dict:
            if handful_dict[colour] > capacity[colour]:
                possible = False
            power_terms[colour] = max(power_terms[colour], handful_dict[colour])

    if possible:
        id_total += game_no

    power = 1
    for colour in power_terms:
        power *= power_terms[colour]
    ic(gp_part, power_terms, power)
    power_sum += power

ic(id_total, power_sum)
