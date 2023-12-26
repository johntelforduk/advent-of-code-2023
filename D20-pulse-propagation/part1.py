# Advent of Code day 20, Pulse Propagation.
# https://adventofcode.com/2023/day/20

from icecream import ic


class FlipFlop:
    # Flip-flop modules (prefix %) are either on or off; they are initially off.
    # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    # However, if a flip-flop module receives a low pulse, it flips between on and off.
    # If it was off, it turns on and sends a high pulse.
    # If it was on, it turns off and sends a low pulse.

    def __init__(self, name: str, destinations: list):
        self.kind = 'FlipFlop'
        self.name = name
        self.destinations = destinations    # List of names of destination modules.
        self.state = 'off'

    def receive(self, received_from: str, pulse: str) -> list:
        assert pulse in ['high', 'low']

        if pulse == 'high':
            return []

        if self.state == 'off':
            self.state = 'on'
            send = 'high'
        else:
            self.state = 'off'
            send = 'low'

        output = []
        for d in self.destinations:
            output.append((self.name, d, send))
            print(f'{self.name}- {send}-> {d}')

        return output

    def status(self):
        return self.state


class Conjunction:
    # Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    # input modules; they initially default to remembering a low pulse for each input.
    # When a pulse is received, the conjunction module first updates its memory for that input.
    # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.

    def __init__(self, name: str, destinations: list):
        self.kind = 'Conjunction'
        self.name = name
        self.destinations = destinations

        # Key = name of module that sent pulse. Value = was the pulse "low" or "high".
        self.memory = {}

    def set_memory(self, source: str):
        self.memory[source] = None

    def receive(self, received_from: str, pulse: str) -> list:
        assert pulse in ['high', 'low']

        self.memory[received_from] = pulse

        all_high = True
        for rf in self.memory:
            if self.memory[rf] != 'high':
                all_high = False

        if all_high:
            send = 'low'
        else:
            send = 'high'

        output = []
        for d in self.destinations:
            output.append((self.name, d, send))
            print(f'{self.name} -{send}-> {d}')

        return output

    def status(self):
        return self.memory


class Broadcast:
    # There is a single broadcast module (named broadcaster).
    # When it receives a pulse, it sends the same pulse to all of its destination modules.

    def __init__(self, name: str, destinations: list):
        self.kind = 'Broadcast'
        self.name = name
        self.destinations = destinations

    def receive(self, received_from: str, pulse: str) -> list:
        assert pulse in ['high', 'low']

        output = []
        for d in self.destinations:
            output.append((self.name, d, pulse))
            print(f'{self.name} -{pulse}-> {d}')
        return output

    def status(self):
        return ''


def count_pulses(pulse_list: list, kind: str) -> int:
    count = 0
    for _, _, this in pulse_list:
        if this == kind:
            count += 1
    return count


with open('input.txt', 'r') as file:
    config_str = file.read()

config = {}

for line in config_str.split('\n'):
    module_str, destinations_str = line.split(' -> ')

    destinations = [d for d in destinations_str.split(', ')]
    ic(module_str, destinations)

    if module_str == 'broadcaster':
        config[module_str] = Broadcast(name=module_str, destinations=destinations)
    else:
        kind = module_str[0]
        name = module_str[1:]
        if kind == '%':
            config[name] = FlipFlop(name=name, destinations=destinations)
        else:
            assert kind == '&'
            config[name] = Conjunction(name=name, destinations=destinations)

for source in config:
    for destination in config[source].destinations:
        if destination in config:
            if config[destination].kind == 'Conjunction':
                config[destination].set_memory(source)

count_low, count_high = 0, 0

for presses in range(1000):
    print('\nbutton -low-> broadcaster')
    bus = [('button', 'broadcaster', 'low')]
    count_low += 1

    while len(bus) != 0:
        source_name, target_name, pulse = bus.pop(0)
        if target_name in config:
            target = config[target_name]
            new_pulses = target.receive(received_from=source_name, pulse=pulse)
            config[target_name] = target
            count_low += count_pulses(pulse_list=new_pulses, kind='low')
            count_high += count_pulses(pulse_list=new_pulses, kind='high')
            bus = bus + new_pulses

for thing in config:
    ic(thing, config[thing].status())

ic(count_low, count_high, count_low * count_high)
