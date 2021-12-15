import heapq
import sys


# For ease of visualizing
def print_graph(g):
    for y in range(len(g)):
        for x in range(len(g[0])):
            print(str(g[y][x]).ljust(5), end='')
        print()


def nbrs(x, y, max_x, max_y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if 0 <= x + dx <= max_x and 0 <= y + dy <= max_y:
            yield (x + dx, y + dy)


def manhattan(x, y, max_x, max_y):
    return abs(x - max_x) + abs(y - max_y)


def manhattan_s(*args, s=5):
    return s*manhattan(*args)


def euclidean(x, y, max_x, max_y):
    return ((x - max_x)**2 + (y - max_y)**2)**0.5


def identity(*args):
    return 0


def part1(G, dist=manhattan):
    max_x, max_y = len(G[0])-1, len(G)-1
    # Using A*, we will create a heuristic H where H[y][x] is the cost to
    # reach the goal from (x, y) (Manhattan distance here)
    # TODO: is manhattan the best choice?
    # TODO: ensure heuristic is _admissible_ (never over-estimates cost to goal)
    H = [[dist(x, y, max_x, max_y)
          for x in range(max_x + 1)]
         for y in range(max_y + 1)]

    # We will keep track of the lowest cost so far to reach (x, y), and
    # store this in a min heap sorted by the cost_so_far + heuristic
    # [cost+heuristic, cost, coord]
    pq = [[sys.maxsize, sys.maxsize, (x, y)]
          for x in range(max_x + 1)
          for y in range(max_y + 1)]
    pq[0][1] = 0
    pq[0][0] = pq[0][1] + H[0][0]

    # We also need a mapping from node to cost vector in the heap to look up
    # neighbours' costs
    costs = {v[-1]: v for v in pq}

    goal = (max_x, max_y)
    while pq:
        h_cost, cost_to_current, (x, y) = heapq.heappop(pq)
        if cost_to_current == sys.maxsize:
            raise RuntimeError('graph is disconnected?')
        if (x, y) == goal:
            # we're done
            return cost_to_current
        # N.B. we should never have a cycle by nature of the algorithm
        changed = False
        for (nx, ny) in nbrs(x, y, max_x, max_y):
            _heuristic_cost_n, cost_n, _ = costs[(nx, ny)]
            cost_with_current = cost_to_current + G[ny][nx]
            if cost_with_current < cost_n:
                changed = True
                # we found a shorter path
                costs[(nx, ny)][0] = cost_with_current + H[ny][nx]
                costs[(nx, ny)][1] = cost_with_current
        # redistribute heap
        if changed:
            heapq.heapify(pq)

    raise RuntimeError('no nodes left?')




def part2(G):
    pass


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().splitlines()

    G = [[int(n) for n in line] for line in content]

    val1 = part1(G)
    print('Part 1:', val1)

    val2 = part2(G)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
