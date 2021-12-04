import sys


def movement_to_coord_p1(direction, n):
    # horizonals, depth
    if direction == 'forward':
        return [n, 0]
    elif direction == 'down':
        return [0, n]
    elif direction == 'up':
        return [0, -n]


def movement_to_coord_p2(direction, n):
    # horizonals, aim
    if direction == 'forward':
        return [n,  0]
    elif direction == 'down':
        return [0,  n]
    elif direction == 'up':
        return [0,  -n]


def part1(data):
    deltas = [movement_to_coord_p1(*m) for m in data]
    dxs, dzs = list(zip(*deltas))
    return sum(dxs) * sum(dzs)


def part2(data):
    deltas = [movement_to_coord_p2(*m) for m in data]
    # horizontal, depth, aim
    pos = [0, 0, 0]
    for dx, da in deltas:
        pos[0] += dx
        pos[1] += pos[2]*dx
        pos[2] += da

    return pos[0]*pos[1]


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()

    data = [l.split() for l in content]
    data = [(e1, int(e2)) for e1, e2 in data]

    val1 = part1(data)
    print('Part 1:', val1)

    val2 = part2(data)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
