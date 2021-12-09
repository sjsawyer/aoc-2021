import sys
from functools import reduce


def get_nbrs(data, i, j, coords=False):
    nbrs = []
    for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        ii, jj = i + di, j + dj
        if ii < 0 or jj < 0 or ii == len(data) or jj == len(data[0]):
            continue
        if coords:
            # for part 2
            nbrs.append((ii, jj))
        else:
            nbrs.append(data[ii][jj])
    return nbrs


def part1(data):
    min_coords = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            nbrs = get_nbrs(data, i, j)
            if data[i][j] < min(nbrs):
                min_coords.append((i, j))

    risk_level = (
        sum(data[c[0]][c[1]] + 1 for c in min_coords)
    )
    return risk_level, min_coords


def part2(data, min_coords):
    # depth first search
    basin_sizes = []

    for i, j in min_coords:
        basin_size = 0
        seen = {(i, j)}
        to_explore = [(i, j)]

        # depth first search
        while to_explore:
            ci, cj = to_explore.pop()
            basin_size += 1
            nbrs = get_nbrs(data, ci, cj, coords=True)
            for ni, nj in nbrs:
                if data[ni][nj] == 9 or (ni, nj) in seen:
                    continue
                seen.add((ni, nj))
                to_explore.append((ni, nj))

        basin_sizes.append(basin_size)

    largest_3 = sorted(basin_sizes)[-3:]
    return reduce(lambda x, y: x*y, largest_3)


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()

    data = [[int(n) for n in line.strip()] for line in content]

    val1, min_coords = part1(data)
    print('Part 1:', val1)

    val2 = part2(data, min_coords)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
