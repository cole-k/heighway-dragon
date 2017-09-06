import png
import math
import numpy as np
# from itertools import combinations
# import sys


class Coord():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, coord):
        return Coord(self.x + coord.x, self.y + coord.y)

    def __str__(self):
        return str((self.x, self.y))

    def __mul__(self, scalar):
        if type(scalar) is int or type(scalar) is float:
            return Coord(self.x * scalar, self.y * scalar)
        else:
            raise ValueError("Coordinates may only be multiplied by scalars.")

    # Only use this for unit vectors
    def rotate_left(self):
        # If x == 0, we're facing up or down, and rotating left requires us
        # to negate y and flip the coordinates
        if self.x == 0:
            self.x = -1 * self.y
            self.y = 0
        else:
            self.y = self.x
            self.x = 0

    # Only use this for unit vectors
    def rotate_right(self):
        # If x == 0, we're facing left or right, and rotating right requires us
        # to negate x and flip the coordinates
        if self.y == 0:
            self.y = -1 * self.x
            self.x = 0
        else:
            self.x = self.y
            self.y = 0


class Walker():

    def __init__(self, dragon_str):
        self.position = Coord(0, 0)
        self.direction = Coord(1, 0)
        self.dragon_str = dragon_str

    def walk(self):
        output = [self.position, self.position + self.direction]
        for direction in self.dragon_str:
            if direction == 1:
                self.direction.rotate_left()
            elif direction == 0:
                self.direction.rotate_right()
            output.append(output[-1] + self.direction)
        return output


def complement_center(binary_string):
    s = binary_string.copy()
    center = (len(binary_string)-1)//2
    s[center] = 1 - s[center]
    return s


def dragon_string(iterations, seed=[1]):
    string = seed.copy()
    for _ in range(iterations):
        string = string + [1] + complement_center(string)
    return string


def draw_straight_line(point_a, point_b, grid, stroke=0):
    # vertical line
    if point_a.x == point_b.x:
        start_val = min(point_a.y, point_b.y)
        for i in range(abs(point_b.y - point_a.y) + 1):
            if stroke == 0:
                grid[point_a.x][start_val + i] = 1
            else:
                grid[point_a.x][start_val + i] += stroke
    # horizontal line
    if point_a.y == point_b.y:
        start_val = min(point_a.x, point_b.x)
        for i in range(abs(point_b.x - point_a.x) + 1):
            if stroke == 0:
                grid[start_val + i][point_a.y] = 1
            else:
                grid[start_val + i][point_a.y] += stroke


def binarize(grid):
    g = grid.copy()
    for i in range(len(g)):
        for j in range(len(g[0])):
            g[i][j] = g[i][j] != 0
    return g


def extract_bits(number, start, n_bits):
    mask = ((1 << n_bits) - 1) << start
    return (number & mask) >> start

def colorize(grid, color, background):
    g = grid.copy()
    for i in range(len(g)):
        for j in range(len(g[0])):
            # red = extract_bits(i, 3, 6)
            # green = (extract_bits(i, 0, 3) << 3) + extract_bits(j, 6, 3)
            # blue = extract_bits(j, 0, 6)
            # factor = 255 // 63
            # g[i][j] = [red * factor, green * factor, blue * factor] if g[i][j] != 0 else list(background)
            factor = .75 * (i / len(g))
            g[i][j] = list(map(lambda c: math.floor(c * (factor + 0.25) ), color)) \
                if g[i][j] != 0 else list(background)
    # flatten lists
    g = list(map(lambda row: sum(row,[]),g))
    return g

if __name__ == '__main__':
    iterations, stretch_factor, seed = 19, 1, None

    w = Walker(dragon_string(iterations, seed if seed else [1]))

    fractal = w.walk()

    x_vals = list(map(lambda c: c.x, fractal))
    y_vals = list(map(lambda c: c.y, fractal))

    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)

    adjustment = Coord(-1 * min_x, -1 * min_y)

    print(min_x, max_x, min_y, max_y)
    grid = [[0 for _ in range((max_y - min_y) * stretch_factor + 1)]
            for _ in range((max_x - min_x) * stretch_factor + 1)]

    # grid = np.asarray(grid)

    for i in range(len(fractal) - 1):
        point_a = (fractal[i] + adjustment) * stretch_factor
        point_b = (fractal[i + 1] + adjustment) * stretch_factor
        draw_straight_line(point_a, point_b, grid)

    # colors = list(combinations(range(64), 3))
    # colors = sorted(colors, key=lambda t: (t[0]*t[1]*t[2],) + t)
    # colors = (255 // 63) * np.asarray(colors)
    # print(colors)

    with open('output.png', 'wb') as f:
        # w = png.Writer(len(grid[0]), len(grid), palette=[(230, 232, 235),
        #                                                  (60, 128, 200)])
        # w.write(f, binarize(grid))
        w = png.Writer(len(grid[0]), len(grid))
        w.write(f, colorize(grid, (117, 190, 240), (37,41,49)))
