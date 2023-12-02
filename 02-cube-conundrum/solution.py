# Advent of code day 2, Cube Conundrum.
# https://adventofcode.com/2023/day/2

from icecream import ic

with open('input.txt', 'r') as file:
    games = file.read()

capacity = {'red': 12, 'green': 13, 'blue': 14}
id_total = 0

for game in games.split('\n'):
    gn_part, gp_part = game.split(': ')
    game_no = int(gn_part.split(' ')[1])
    ic(gn_part, gp_part, game_no)

    possible = True
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

    if possible:
        id_total += game_no

ic(id_total)
