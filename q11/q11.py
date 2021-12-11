import copy
import sys


def nbrs(coord, max_x, max_y):
    x, y = coord
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 0 <= i <= max_x and 0 <= j <= max_y and (i, j) != (x, y):
                yield (i, j)


def flash(c, coords, max_x, max_y):
    flashes = 0

    if coords[c] == 0:
        # we've flashed before
        return flashes

    coords[c] += 1
    if coords[c] > 9:
        # we are flashing
        flashes += 1
        coords[c] = 0
        for nbr in nbrs(c, max_x, max_y):
            flashes += flash(nbr, coords, max_x, max_y)

    return flashes


def part1(coords, max_x, max_y, steps=10):
    flashes = 0

    for step in range(steps):
        for c in coords:
            coords[c] += 1

        for c in coords:
            if coords[c] > 9:
                flashes += flash(c, coords, max_x, max_y)

    return flashes


def part2(coords, max_x, max_y):
    steps = 0

    while True:
        steps += 1
        flashes = 0

        for c in coords:
            coords[c] += 1

        for c in coords:
            if coords[c] > 9:
                flashes += flash(c, coords, max_x, max_y)

        if flashes == (max_x+1) * (max_y+1):
            print_coords(coords, max_x, max_y)
            return steps


def print_coords(coords, max_x, max_y):
    for i in range(0, max_x+1):
        print([coords[(i, j)] for j in range(0, max_y+1)])
    print()


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    coords = {}
    for y, line in enumerate(content.splitlines()):
        for x, val in enumerate(line):
            coords[(x, y)] = int(val)
    max_x, max_y = x, y

    val1 = part1(copy.deepcopy(coords), max_x, max_y, steps=100)
    print('Part 1:', val1)

    val2 = part2(coords, max_x, max_y)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
