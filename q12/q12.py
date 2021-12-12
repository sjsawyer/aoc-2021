import sys
from collections import defaultdict


def part1(g):

    visited = defaultdict(lambda: 0)

    def num_paths(node):
        if node == 'end':
            return 1

        visited[node] += 1
        from_here = 0
        for w in g[node]:
            if not visited[w] or w.isupper():
                from_here += num_paths(w)

        # backtrack
        visited[node] -= 1

        return from_here

    return num_paths('start')


def part2(g):

    visited = defaultdict(lambda: 0)

    def num_paths(node):
        if node == 'end':
            return 1

        visited[node] += 1
        from_here = 0
        for w in g[node]:
            if (
                w.isupper()
                or not visited[w]
                # w is small cave, can visit as long as no other small caves
                # have been visited more than once
                or (not any(
                    visited[j] > 1 for j in visited
                    if j not in {'start', 'end'}
                    and j.islower()
                ) and w not in {'start', 'end'})
            ):
                from_here += num_paths(w)

        # backtrack
        visited[node] -= 1

        return from_here

    return num_paths('start')


def main(input_file):
    with open(input_file, 'r') as f:
        content = [l.strip() for l in f.readlines()]

    # represent as adjacency list
    g = defaultdict(set)
    for line in content:
        v, w = line.split('-')
        g[v].add(w)
        g[w].add(v)

    val1 = part1(g)
    print('Part 1:', val1)

    val2 = part2(g)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
