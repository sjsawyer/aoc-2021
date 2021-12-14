import sys
from collections import defaultdict


def evolve_sequence(s0, inserts, steps):
    # just count the pairs at each iteration
    counts = defaultdict(lambda: 0)
    # edge cases for later
    edges = (s0[0], s0[-1])
    for i in range(len(s0)-1):
        counts[s0[i:i+2]] += 1

    for _ in range(steps):
        new_counts = defaultdict(lambda: 0)
        for pair in counts:
            a, b = pair
            c = inserts[pair]
            new_counts[a+c] += counts[pair]
            new_counts[c+b] += counts[pair]
        counts = new_counts

    letters = set(''.join(pair for pair in counts))
    totals = {}
    for letter in letters:
        total = sum(counts[pair] for pair in counts if letter in pair)
        # also need to add doubles again to avoid undercounting
        total += sum(
            counts[pair] for pair in counts if pair == letter + letter)
        # now divide by 2 since a single element belongs to 2 pairs
        total = int(total / 2)
        # in the case of the edges, we've under counted by 1
        if letter in edges:
            total += 1
        totals[letter] = total

    # sort totals by value
    frequencies = sorted(totals.values())
    return frequencies[-1] - frequencies[0]


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    s0, inserts_s = content.split('\n\n')
    inserts = {}
    for s in inserts_s.splitlines():
        pair, insert = s.split(' -> ')
        inserts[pair] = insert

    val1 = evolve_sequence(s0, inserts, 10)
    print('Part 1:', val1)

    val2 = evolve_sequence(s0, inserts, 40)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
