# Advent of Code day 10, Pipe Maze.
# https://adventofcode.com/2023/day/10

from icecream import ic
import pygame


def escape(x: int, y:int, mx: int, my: int, loop: list, tried: list) -> bool: #      cs: set, c, tried: set):
    """Return True if there is a path from the parm co-ordinate (x, y) to escape from the map, without visiting
    one of the previously tried tiles. Otherwise return False."""

    # We've escaped!
    if x < 0 or x > mx or y < 0 or y > mx:
        return True

    # We hit a bit of the pipeline loop.
    if (x, y) in loop:
        return False

    # Attempt escape in all possible directions.
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) not in tried:
            tried.append((new_x, new_y))
            # if escape(cs, c=(x + dx, y + dy, z + dz), tried=tried):
            if escape(x=new_x, y=new_y, mx=mx, my=my, loop=loop, tried=tried):
                return True

    # No escape.
    return False


with open('test6.txt', 'r') as file:
    tiles_str = file.read()

# Key = tuple, (x, y), position of the tile.
# Value = tile string.
tiles = {}

sx, sy, = None, None                # Co-ordinates of the start square 'S'.
mx, my = 0, 0                       # Max x and y in the map.

for line in tiles_str.split('\n'):
    mx = 0
    for x in line:
        tiles[(mx, my)] = x
        if x == 'S':
            sx, sy = mx, my
        mx += 1
    my += 1

mx -= 1
my -= 1

ic(sx, sy)

visited = []
done = False
x, y = sx, sy
fx, fy = None, None
length = 0

try_order = 'WSNE'

while not done:

    # ic(x, y)
    moved = False

    for direction in try_order:

        if direction == 'N' and not moved:
            if (x, y - 1) not in visited and (x, y - 1) in tiles:
                if tiles[(x, y)] in "S|LJ" and tiles[(x, y - 1)] in "S|7F":
                    y = y - 1
                    moved = True

        if direction == 'W' and not moved:
            if (x - 1, y) not in visited and (x - 1, y) in tiles:
                if tiles[(x, y)] in "S-J7" and tiles[(x - 1, y)] in "S-LF":
                    x = x - 1
                    moved = True

        if direction == 'E' and not moved:
            if (x + 1, y) not in visited and (x + 1, y) in tiles:
                if tiles[(x, y)] in "S-LF" and tiles[(x + 1, y)] in "S-J7":
                    x = x + 1
                    moved = True

        if direction == 'S' and not moved:
            if (x, y + 1) not in visited and (x, y + 1) in tiles:
                if tiles[(x, y)] in "S|7F" and tiles[(x, y + 1)] in "S|LJ":
                    y = y + 1
                    moved = True

    if moved:
        visited.append((x, y))
    else:
        done = True

    length += 1
    done = (x == sx and y == sy)


ic(escape(x=12, y=4, mx=mx, my=my, loop=visited, tried=[]))
ic(escape(x=0, y=1, mx=mx, my=my, loop=visited, tried=[]))
ic(escape(x=14, y=3, mx=mx, my=my, loop=visited, tried=[]))



border = 10
scale = 8

pygame.init()                                               # Initialize the game engine.

screen_size = [scale * (mx + 1) + border * 2, scale * (my + 1) + border * 2]  # [width, height]
screen = pygame.display.set_mode(screen_size)

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
grey = (128, 128, 128)
blue = (0, 0, 255)
red = (255, 0, 0)

screen.fill(white)
enclosed = 0

for y in range(my + 1):
    ic(y)
    for x in range(mx + 1):

        if (x, y) in visited:
            colour = green
        else:
            if escape(x=x, y=y, mx=mx, my=my, loop=visited, tried=[]):
                colour = grey
            else:
                colour = blue
                enclosed += 1


        if x == sx and y == sy:
            pygame.draw.rect(screen, red, (border + x * scale, border + y * scale, scale - 1, scale - 1))

        elif tiles[x, y] == '.':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.375, border + y * scale + scale * 0.375, scale * 0.25, scale * 0.25))

        elif tiles[x, y] == '-':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale -1, scale * 0.5 - 1))

        elif tiles[x, y] == '|':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5 - 1, scale - 1))

        elif tiles[x, y] == 'L':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.75 - 1, scale * 0.5 - 1))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5 - 1, scale * 0.75 - 1))

        elif tiles[x, y] == 'J':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale * 0.75 - 1, scale * 0.5 - 1))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5 - 1, scale * 0.75 - 1))

        elif tiles[x, y] == 'F':
            pygame.draw.rect(screen, colour, (border + x * scale + scale / 4, border + y * scale + scale * 0.25, scale * 0.75 - 1, scale * 0.5 - 1))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.5 - 1, scale * 0.75 - 1))

        elif tiles[x, y] == '7':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale * 0.75 - 1, scale * 0.5 - 1))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.5 - 1, scale * 0.75 - 1))


screenshot_name = 'd10' + '.png'
pygame.image.save(screen, screenshot_name)

pygame.display.flip()

ic(length // 2, enclosed)
