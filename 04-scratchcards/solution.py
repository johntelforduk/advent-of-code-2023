# Advent of code day 4, Scratchcards..
# https://adventofcode.com/2023/day/4

from icecream import ic

with open('input.txt', 'r') as file:
    scratchards = file.read()

total = 0
for row in scratchards.split('\n'):
    numbers = row.split(':')[1]
    two_halves = numbers.split('|')
    winners = [int(number) for number in two_halves[0].split()]
    my_numbers = [int(number) for number in two_halves[1].split()]
    ic(row, winners, my_numbers)

    this_card = 0
    for number in my_numbers:
        if number in winners:
            if this_card == 0:
                this_card = 1
            else:
                this_card *= 2
    total += this_card

ic(total)
