# Advent of code day 7, part 2, Camel Cards.
# https://adventofcode.com/2023/day/7

from icecream import ic
from itertools import product


def find_type(hand: str) -> int:
    distribution = {}
    for card in hand:
        if card in distribution:
            distribution[card] += 1
        else:
            distribution[card] = 1

    multiples = {}
    for card in distribution:
        count = distribution[card]
        if count in multiples:
            multiples[count] += 1
        else:
            multiples[count] = 1

    if 5 in multiples:
        return 90                               # Five of a kind.
    if 4 in multiples:
        return 80                               # Four of a kind.
    if 3 in multiples and 2 in multiples:
        return 70                               # Full house.
    if 3 in multiples:
        return 60                               # Three of a kind.
    if 2 in multiples:
        if multiples[2] == 2:
            return 50                           # Two pair.
        else:
            return 40                           # One pair.
    return 30                                   # High card.


def best_type(hand: str) -> int:
    pos, joker_positions = 0, []
    for card in hand:
        if card == 'J':
            joker_positions.append(pos)
        pos += 1

    if len(joker_positions) == 0:
        return find_type(hand)

    best = 0
    for possible in product('AKQT98765432', repeat=len(joker_positions)):
        possible_list = list(possible)
        # ic(hand, possible, joker_positions)

        pos = 0
        for sub_pos in joker_positions:
            hand = hand[:sub_pos] + possible_list[pos] + hand[sub_pos + 1:]
            pos += 1

        best = max(best, find_type(hand))

    return best

def card_to_num(card: str) -> int:
    picture_to_num = {'A': 24,
                      'K': 23,
                      'Q': 22,
                      'J': 11,                  # Change for Part 2.
                      'T': 20}
    if card in picture_to_num:
        return picture_to_num[card]
    return 10 + int(card)


def hand_to_num(hand: str) -> int:
    hand_int_list = [card_to_num(card) for card in hand]

    hand_value = best_type(hand)
    for card_num in hand_int_list:
        hand_value *= 100
        hand_value += card_num

    ic(hand, hand_value)
    return hand_value


with open('input.txt', 'r') as file:
    hands = file.read()

hands_list = []
for line in hands.split('\n'):
    hand, bid = line.split(' ')
    hands_list.append((hand_to_num(hand), hand, int(bid)))

hands_list.sort()
ic(hands_list)

rank, total_winnings = 1, 0
for _, hand, bid in hands_list:
    total_winnings += rank * bid
    rank += 1

ic(total_winnings)