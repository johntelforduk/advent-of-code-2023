# Advent of code day 6. Wait For It.
# https://adventofcode.com/2023/day/6

from icecream import ic

with open('input.txt', 'r') as file:
    document = file.read()

rows_lists = []
for row in document.split('\n'):
    rows_lists.append([int(term) for term in row.replace('Time:', '').replace('Distance:', '').split()])

races = list(zip(rows_lists[0], rows_lists[1]))
ic(rows_lists, races)

result = 1
for duration, record in races:
    possible_wins = 0
    for button_hold in range(duration):
        distance = button_hold * (duration - button_hold)
        if distance > record:
            possible_wins += 1
    result *= possible_wins

ic(result)
