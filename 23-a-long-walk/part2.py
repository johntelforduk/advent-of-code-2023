# Advent of Code day 23, part 2, A Long Walk.
# https://adventofcode.com/2023/day/23

from icecream import ic
import functools


# From, https://medium.com/@nkhaja/memoization-and-decorators-with-python-32f607439f84
def memoize(func):
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func


def hills_around(trails: dict, x: int, y: int, direction: str) -> list:
    around = []
    for dx, dy, slope, new_direction, double_back in [(0, -1, '^v', 'N', 'S'),
                                         (0, 1, 'v^', 'S', 'N'),
                                         (1, 0, '><', 'E', 'W'),
                                         (-1, 0, '><', 'W', 'E')]:
        if trails[(x + dx, y + dy)] in slope:
            around.append(new_direction)

    if len(around) < 2:
        return []
    return around



def route(x, y, end_x, end_y, so_far, visited, legs) -> int:
    global longest
    # global get_here
    # ic(visited, x, y)

    # ic(x, y)

    if (x, y) == (end_x, end_y):
        if so_far > longest:
            ic(so_far)
            longest = so_far
        return so_far

    if (x, y) in visited:
        return -1000

    # if (x, y) in get_here:
    #     if get_here[(x, y)] > so_far:
    #         ic('give up')
    #         return -1000
    # get_here[(x, y)] = so_far

    possible = []
    for (from_x, from_y, to_x, to_y, steps) in legs:
        if (x, y) == (from_x, from_y):
            possible.append((to_x, to_y, steps))

    assert(len(possible)) <= 4

    new_visited = visited.copy()
    new_visited.append((x, y))

    if len(possible) == 1:
        to_x, to_y, steps = possible[0]
        return route(to_x, to_y, end_x, end_y, so_far + steps, new_visited, legs)

    elif len(possible) == 2:
        to_x1, to_y1, steps1 = possible[0]
        to_x2, to_y2, steps2 = possible[1]
        return max(route(to_x1, to_y1, end_x, end_y, so_far + steps1, new_visited, legs),
                   route(to_x2, to_y2, end_x, end_y, so_far + steps2, new_visited, legs)
                   )

    elif len(possible) == 3:
        to_x1, to_y1, steps1 = possible[0]
        to_x2, to_y2, steps2 = possible[1]
        to_x3, to_y3, steps3 = possible[2]

        return max(route(to_x1, to_y1, end_x, end_y, so_far + steps1, new_visited, legs),
                   route(to_x2, to_y2, end_x, end_y, so_far + steps2, new_visited, legs),
                   route(to_x3, to_y3, end_x, end_y, so_far + steps3, new_visited, legs)
        )

    elif len(possible) == 4:
        to_x1, to_y1, steps1 = possible[0]
        to_x2, to_y2, steps2 = possible[1]
        to_x3, to_y3, steps3 = possible[2]
        to_x4, to_y4, steps4 = possible[3]

        return max(route(to_x1, to_y1, end_x, end_y, so_far + steps1, new_visited, legs),
                   route(to_x2, to_y2, end_x, end_y, so_far + steps2, new_visited, legs),
                   route(to_x3, to_y3, end_x, end_y, so_far + steps3, new_visited, legs),
                   route(to_x4, to_y4, end_x, end_y, so_far + steps4, new_visited, legs)
        )



with open('input.txt', 'r') as file:
    trails_str = file.read()

trails = {}
y = 0
for line in trails_str.split('\n'):
    x = 0
    y += 1
    for c in line:
        x += 1
        trails[(x, y)] = c

end_x, end_y = x - 1, y

legs = set()
legs_to_measure = [(2, 1, 'S')]

while len(legs_to_measure) != 0:
    start_x, start_y, direction = legs_to_measure.pop()
    x, y, steps = start_x, start_y, 0

    done = False
    junction = []
    while not done and len(junction) == 0:
        # ic(x, y, direction)

        dx, dy = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}[direction]
        x, y = x + dx, y + dy

        if (x, y) == (end_x, end_y):        # Last leg found.
            steps += 1
            legs.add((start_x, start_y, x, y, steps))
            done = True

        elif trails[(x, y)] == '.':           # Simple case.
            steps += 1
            junction = hills_around(trails, x, y, direction)

        # Going in the direction on a steep slope.
        elif trails[(x, y)] in '<>^v':
            if (direction, trails[(x, y)]) in [('N', '^'), ('S', 'v'), ('E', '>'), ('W', '<')]:
                steps += 1
            else:
                done = True

        # Go round a corner.
        elif trails[(x, y)] == '#':
            if direction == 'N':
                if trails[(x - 1, y + 1)] in '.<':
                    direction = 'W'
                    x, y = x - dx, y - dy
                elif trails[(x + 1, y + 1)] in '.>':
                    direction = 'E'
                    x, y = x - dx, y - dy

            elif direction == 'S':
                if trails[(x - 1, y - 1)] in '.<':
                    direction = 'W'
                    x, y = x - dx, y - dy
                elif trails[(x + 1, y - 1)] in '.>':
                    direction = 'E'
                    x, y = x - dx, y - dy

            elif direction == 'E':
                if trails[(x - 1, y - 1)] in '.^':
                    direction = 'N'
                    x, y = x - dx, y - dy
                elif trails[(x - 1, y + 1)] in '.v':
                    direction = 'S'
                    x, y = x - dx, y - dy

            elif direction == 'W':
                if trails[(x + 1, y - 1)] in '.^':
                    direction = 'N'
                    x, y = x - dx, y - dy
                elif trails[(x + 1, y + 1)] in '.v':
                    direction = 'S'
                    x, y = x - dx, y - dy

    for d in junction:
        legs.add((start_x, start_y, x, y, steps))
        legs_to_measure.append((x, y, d))


ic(legs_to_measure, end_x, end_y, legs)

extras = set()
for (x1, y1, x2, y2, d) in legs:
    extras.add((x2, y2, x1, y1, d))
legs = legs.union(extras)
ic(legs)

longest = 0
ic(route(x=2, y=1, end_x=end_x, end_y=end_y, so_far=0, visited=[], legs=legs))

