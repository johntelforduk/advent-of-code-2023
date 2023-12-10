# Advent of Code day 10, part 2, Pipe Maze.
# https://adventofcode.com/2023/day/10

from icecream import ic
import pygame

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
grey = (128, 128, 128)
blue = (0, 0, 255)
red = (255, 0, 0)


# Fill function from here, https://stackoverflow.com/a/41662161
def fill_green(surface, position):
    surf_array = pygame.surfarray.pixels2d(surface)  # Create an array from the surface.
    current_color = surf_array[position]  # Get the mapped integer color value.
    ic(current_color)

    # 'frontier' is a list where we put the pixels that's we haven't checked. Imagine that we first check one pixel and
    # then expand like rings on the water. 'frontier' are the pixels on the edge of the pool of pixels we have checked.
    #
    # During each loop we get the position of a pixel. If that pixel contains the same color as the ones we've checked
    # we paint it with our 'fill_color' and put all its neighbours into the 'frontier' list. If not, we check the next
    # one in our list, until it's empty.

    frontier = [position]
    while len(frontier) > 0:
        x, y = frontier.pop()
        try:  # Add a try-except block in case the position is outside the surface.
            if surf_array[x, y] == surface.map_rgb(green):
                continue
        except IndexError:
            continue
        surf_array[x, y] = surface.map_rgb(green)
        # Then we append the neighbours of the pixel in the current position to our 'frontier' list.
        frontier.append((x + 1, y))  # Right.
        frontier.append((x - 1, y))  # Left.
        frontier.append((x, y + 1))  # Down.
        frontier.append((x, y - 1))  # Up.

    pygame.surfarray.blit_array(surface, surf_array)


with open('input.txt', 'r') as file:
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

border = 10
scale = 8

pygame.init()                                               # Initialize the game engine.

screen_size = [scale * (mx + 1) + border * 2, scale * (my + 1) + border * 2]  # [width, height]
screen = pygame.display.set_mode(screen_size)


screen.fill(white)

for y in range(my + 1):
    ic(y)
    for x in range(mx + 1):

        if (x, y) in visited:
            colour = green
        else:
            colour = grey

        if x == sx and y == sy:
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale, scale, scale))

        elif tiles[x, y] == '.':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.375, border + y * scale + scale * 0.375, scale * 0.25, scale * 0.25))

        elif tiles[x, y] == '-':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale, scale * 0.5))

        elif tiles[x, y] == '|':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5, scale))

        elif tiles[x, y] == 'L':
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.75, scale * 0.5))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5, scale * 0.75))

        elif tiles[x, y] == 'J':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale * 0.75, scale * 0.5))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale , scale * 0.5, scale * 0.75))

        elif tiles[x, y] == 'F':
            pygame.draw.rect(screen, colour, (border + x * scale + scale / 4, border + y * scale + scale * 0.25, scale * 0.75, scale * 0.5))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.5, scale * 0.75))

        elif tiles[x, y] == '7':
            pygame.draw.rect(screen, colour, (border + x * scale, border + y * scale + scale * 0.25, scale * 0.75, scale * 0.5))
            pygame.draw.rect(screen, colour, (border + x * scale + scale * 0.25, border + y * scale + scale * 0.25, scale * 0.5, scale * 0.75))


# screen.set_at((70, 50), black)
# ic(screen.get_at((71, 50)) == black)
# flood(70, 50, screen)

fill_green(screen, (570, 570))

screenshot_name = 'd10p2' + '.png'
pygame.image.save(screen, screenshot_name)

enclosed = 0
for y in range(my + 1):
    ic(y)
    for x in range(mx + 1):

        if (x, y) not in visited:
            if screen.get_at((int(border + x * scale + scale * 0.375), int(border + y * scale + scale * 0.375))) == green:
                enclosed += 1

pygame.display.flip()

ic(length // 2, enclosed)
