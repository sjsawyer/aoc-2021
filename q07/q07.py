import sys


def part1(data):

    counts = {d: 0 for d in data}
    for d in data:
        counts[d] += 1

    elements = counts.keys()

    cost = {d: 0 for d in elements}
    for d in elements:
        for other in elements:
            cost[d] += abs(d - other) * counts[other]

    return min(cost.values())


def part2(data):

    counts = {d: 0 for d in data}
    for d in data:
        counts[d] += 1

    # solution can now contain missing elements
    elements = range(min(data), max(data))

    cost = {d: 0 for d in elements}
    for d in elements:
        for other in counts.keys():
            n = abs(d - other)
            cost[d] += int(((n*(n+1))/2) * counts[other])

    return min(cost.values())


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().split(',')

    data = [int(n) for n in content]

    val1 = part1(data)
    print('Part 1:', val1)

    val2 = part2(data)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
