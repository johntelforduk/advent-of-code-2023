# Advent of Code day 25, Snowverload.
# https://adventofcode.com/2023/day/25

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt

with open('input.txt', 'r') as file:
    connections_str = file.read()

G = nx.Graph()

for line in connections_str.split('\n'):
    source, targets = line.split(': ')
    for t in targets.split(' '):
        G.add_edge(source, t)

cut_value, partition = nx.stoer_wagner(G)
ic(cut_value)
ic(len(partition[0] * len(partition[1])))

subax1 = plt.subplot(111)
nx.draw(G, with_labels=True)
plt.show()
