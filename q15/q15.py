import heapq
import sys
from collections import defaultdict
from functools import partial

""" Learnings from this question

1. A* not always faster than Dijkstra.
2. With A*, the heuristic must be _admissible_ in order for the path to be
   optimal (heuristic cannot return a cost remaining greater than that of the
   true cost remaining).
3. Treating entries in the pq as immutable and inserting new entires as they
   come up (while potentially inserting multiple entries per node) as opposed
   to modifying them in place and repeatedly calling heapify() is MUCH faster
   (literally 100x in the case of this example)

"""


def nbrs(x, y, max_x, max_y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= x + dx <= max_x and 0 <= y + dy <= max_y:
            yield (x + dx, y + dy)


def manhattan(x, y, max_x, max_y):
    return abs(x - max_x) + abs(y - max_y)


def identity(*args, **kwargs):
    return 0


def astar(G, dist=identity, scale=1):
    max_x, max_y = max(x for x, _ in G), max(y for _, y in G)
    width, height = max_x + 1, max_y + 1
    width_scaled, height_scaled = width * scale, height * scale

    heuristic = partial(dist, max_x=width_scaled-1, max_y=height_scaled-1)
    gen_nbrs = partial(nbrs, max_x=width_scaled-1, max_y=height_scaled-1)

    start = (0, 0)
    goal = (width_scaled-1, height_scaled-1)

    # This will help replicate the map
    def G_replicated(G, width, height):

        def _eval_G(x, y):
            x0, y0 = x % width, y % height
            dx, dy = x // width, y // height
            return (G[(x0, y0)] + dx + dy - 1) % 9 + 1

        return _eval_G

    eval_G = G_replicated(G, width, height)

    # Current lowest cost to each node
    costs = defaultdict(lambda: sys.maxsize)
    costs[start] = 0
    pq = [(costs[start] + heuristic(*start), start)]

    while pq:
        _heuristic_cost, (x, y) = heapq.heappop(pq)
        cost_to_current = costs[(x, y)]
        assert cost_to_current != sys.maxsize, "Graph disconnected?"
        if (x, y) == goal:
            # we're done
            return cost_to_current
        # N.B. we should never have a cycle by nature of the algorithm
        for (nx, ny) in gen_nbrs(x, y):
            cost_with_current = cost_to_current + eval_G(nx, ny)
            if cost_with_current < costs[(nx, ny)]:
                # We found a shorter path. Pushing onto heap will naturally
                # "replace" the previous instance of (nx, ny) by inserting
                # above it
                costs[(nx, ny)] = cost_with_current
                heapq.heappush(
                    pq, (cost_with_current + heuristic(nx, ny), (nx, ny)))

    assert False, "No path found"


def main(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    G = {(x, y): int(v)
         for y, line in enumerate(lines)
         for x, v in enumerate(line)}

    val1 = astar(G)
    print('Part 1:', val1)

    val2 = astar(G, scale=5)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
