import re
import sys
from collections import defaultdict


def get_num_overlapping_points(lines):
    counts = defaultdict(lambda: 0)
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            # hortizonal
            y11, y22 = (y1, y2) if y2 > y1 else (y2, y1)
            for y in range(y11, y22 + 1):
                counts[(x1, y)] += 1
        elif y1 == y2:
            # vert
            x11, x22 = (x1, x2) if x2 > x1 else (x2, x1)
            for x in range(x11, x22 + 1):
                counts[(x, y1)] += 1
        elif x1 - x2 == y1 - y2 or x1 - x2 == -(y1 - y2):
            # diagonal
            xs = (
                range(x1, x2 + 1) if x2 > x1 else range(x1, x2 - 1, -1)
            )
            ys = (
                range(y1, y2 + 1) if y2 > y1 else range(y1, y2 - 1, -1)
            )
            for (x, y) in zip(xs, ys):
                counts[(x, y)] += 1

    return sum(v > 1 for v in counts.values())


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    lines = (map(int, nums)
             for nums in re.findall(r'(\d+),(\d+) -> (\d+),(\d+)', content))
    lines = [((x1, y1), (x2, y2))
             for x1, y1, x2, y2 in lines]

    val1 = get_num_overlapping_points(
        [((x1, y1), (x2, y2)) for ((x1, y1), (x2, y2)) in lines
         if x1 == x2 or y1 == y2]
    )
    print('Part 1:', val1)

    val2 = get_num_overlapping_points(lines)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
