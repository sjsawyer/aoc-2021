import sys


def part1(content):
    cc = list(zip(*content))
    gamma_str = ''.join(
        (str(int(sum(map(int, l)) > len(cc[0]) // 2))
         for l in cc)
    )
    epsilon_str = ''.join('0' if c == '1' else '1' for c in gamma_str)
    return int(gamma_str, 2) * int(epsilon_str, 2)


def part1_bitlogic(content):

    nbits = len(content[0])
    data = [int(s, 2) for s in content]

    def list_to_bin(l):
        return int(''.join(map(str, l)), 2)

    gamma = [0] * nbits
    epsilon = [0] * nbits

    len_ = len(data)
    for i in range(nbits):
        sum_ = 0
        for n in data:
            sum_ += bool(n & (1 << i))
        gamma[i] += (sum_ > len_ // 2)
        epsilon[i] += (gamma[i] ^ 1)

    return list_to_bin(reversed(gamma)) * list_to_bin(reversed(epsilon))


def part2(content):
    cc = [[int(i) for i in row] for row in list(zip(*content))]

    # oxygen generator rating
    ccc = [row[:] for row in cc]
    i = 0
    while len(ccc[0]) != 1:
        if sum(ccc[i]) >= len(ccc[0]) / 2:
            # keep 1s
            ccc = list(zip(*
                [row for row in list(zip(*ccc)) if row[i] == 1]
            ))
        else:
            ccc = list(zip(*
                [row for row in list(zip(*ccc)) if row[i] == 0]
            ))
        i += 1
    ox = int(''.join(str(row[0]) for row in ccc), 2)

    # oxygen generator rating
    ccc = [row[:] for row in cc]
    i = 0
    while len(ccc[0]) != 1:
        if sum(ccc[i]) < len(ccc[0]) / 2:
            # keep 1s
            ccc = list(zip(*
                [row for row in list(zip(*ccc)) if row[i] == 1]
            ))
        else:
            ccc = list(zip(*
                [row for row in list(zip(*ccc)) if row[i] == 0]
            ))
        i += 1
    co2 = int(''.join(str(row[0]) for row in ccc), 2)

    return ox * co2


def main(input_file):
    with open(input_file, 'r') as f:
        content = [l.strip() for l in f.readlines()]

    val1 = part1(content)
    print('Part 1:', val1)

    val2 = part2(content)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
