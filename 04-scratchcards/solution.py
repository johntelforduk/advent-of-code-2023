# Advent of code day 4, Scratchcards..
# https://adventofcode.com/2023/day/4

from icecream import ic

with open('input.txt', 'r') as file:
    scratchards = file.read()

total = 0

# Key = Card number.
# Value = Number of copied of it held.
cards_held = {}

for row in scratchards.split('\n'):
    card_no_str, numbers = row.split(':')
    card_no = int(card_no_str.replace('Card', ''))

    if card_no in cards_held:
        cards_held[card_no] += 1
    else:
        cards_held[card_no] = 1

    two_halves = numbers.split('|')
    winners = [int(number) for number in two_halves[0].split()]
    my_numbers = [int(number) for number in two_halves[1].split()]
    # ic(row, card_no, winners, my_numbers)

    this_card, matches = 0, 0
    for number in my_numbers:
        if number in winners:
            matches += 1
            if this_card == 0:
                this_card = 1
            else:
                this_card *= 2
    total += this_card

    # ic(card_no, matches, cards_held)
    for card_won in range(card_no + 1, card_no + matches + 1):
        # ic(card_won)
        if card_won in cards_held:
            cards_held[card_won] += cards_held[card_no]
        else:
            cards_held[card_won] = cards_held[card_no]

card_count = 0
for card in cards_held:
    card_count += cards_held[card]

ic(total, card_count)
