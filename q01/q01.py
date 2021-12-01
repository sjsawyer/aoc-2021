import sys


def part1(data):
    return sum(((data[i+1] - data[i]) > 0 for i in range(len(data)-1)))


def part2(data):
    windowed = [(data[i] + data[i+1] + data[i+2])
                for i in range(len(data)-2)]
    return part1(windowed)


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()

    data = [int(n) for n in content]

    val1 = part1(data)
    print('Part 1:', val1)

    val2 = part2(data)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
