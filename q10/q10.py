import sys

CLOSE_CHAR = {
    '{': '}',
    '(': ')',
    '<': '>',
    '[': ']',
}

POINTS_1 = {
    '}': 1197,
    ')': 3,
    '>': 25137,
    ']': 57,
}

POINTS_2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def part1_and_part2(lines):
    open_chars = CLOSE_CHAR.keys()
    part1 = 0
    part2_scores = []

    for line in lines:

        seen = []

        for c in line:
            if c in open_chars:
                seen.append(c)
                continue

            expected = CLOSE_CHAR[seen.pop()] if seen else None
            if c != expected:
                # line is corrupted
                part1 += POINTS_1[c]
                break

        else:
            # line is incomplete
            score = 0
            for c in reversed(seen):
                score = (score * 5) + POINTS_2[CLOSE_CHAR[c]]

            part2_scores.append(score)

    part2_scores.sort()
    part2 = part2_scores[len(part2_scores) // 2]

    return part1, part2


def main(input_file):
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    val1, val2 = part1_and_part2(lines)
    print('Part 1:', val1)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
