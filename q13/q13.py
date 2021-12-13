import sys


def fold_paper(coords, folds):
    part1 = None

    for d, amount in folds:

        to_add = set()
        if d == 'x':
            for x, y in list(coords):
                if x > amount:
                    to_add.add((2*amount - x, y))
                    coords.remove((x, y))
        elif d == 'y':
            for x, y in list(coords):
                if y > amount:
                    to_add.add((x, 2*amount - y))
                    coords.remove((x, y))
        for x, y in to_add:
            coords.add((x, y))

        # part 1 we just care about first fold
        part1 = part1 or len(coords)

    # part 2 we just view the message
    part2 = coords
    return part1, part2


def print_coords(coords):

    maxx, maxy = max(x for (x, y) in coords), max(y for (x, y) in coords)

    for j in range(0, maxy+1):
        row = ''.join(
            '#' if (i, j) in coords else '.'
            for i in range(0, maxx+1)
        )
        print(''.join(row))


def main(input_file):
    with open(input_file, 'r') as f:
        coords_s, instructions_s = f.read().split('\n\n')

    coords = set()
    folds = []

    for c in coords_s.splitlines():
        x, y = c.split(',')
        coords.add((int(x), int(y)))
    for inst in instructions_s.splitlines():
        d, amount = inst.split('fold along ')[-1].split('=')
        folds.append((d, int(amount)))

    val1, val2 = fold_paper(coords, folds)
    print('Part 1:', val1)
    print('Part 2:')
    print_coords(val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
