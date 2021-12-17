import sys
import re

def part1(y1, y2):

    def gen_y(v_y):
        y = 0
        while True:
            y += v_y
            yield y
            v_y -= 1

    # note for our input, the trench is below us
    speed = 1
    max_iterations = 100
    max_max_y = -float('inf')
    max_max_y_speed = None

    for _ in range(max_iterations):
        hit = False
        passed = False
        max_y = -float('inf')
        max_y_speed = None

        generator = gen_y(speed)
        while True:
            p = next(generator)
            if p > max_y:
                max_y = p
                max_y_speed = speed

            if y1 <= p <= y2:
                hit = True
                break

            if p < y1:
                passed = True
                break

        if hit:
            if max_y > max_max_y:
                max_max_y = max_y
                max_max_y_speed = max_y_speed

        speed += 1
        hit, passed = False, False

    return max_max_y, max_max_y_speed


def part2(x1, x2, y1, y2, vy_max):
    # Calculate valid ranges for vx and vy

    # vxs
    overshot = False
    vxs = []
    vx = 1
    while vx <= x2:
        x = 0
        s = vx
        while s >= 0:
            x += s
            s -= 1
            if x1 <= x <= x2:
                vxs.append(vx)
                break
        vx += 1

    # vys are easy
    vys = list(range(y1, vy_max+1))

    # now try everything
    valid = []
    for vx_ in vxs:
        for vy_ in vys:
            x, y = 0, 0
            vx, vy = vx_, vy_
            while x <= x2 and y >= y1:
                x += vx
                y += vy
                if x1 <= x <= x2 and y1 <= y <= y2:
                    valid.append((vx, vy))
                    break
                else:
                    vx = max(vx - 1, 0)
                    vy -= 1

    return len(valid)


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().strip()

    x1, x2, y1, y2 = map(int, re.match(
        'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', content
    ).groups())

    val1, vy_max = part1(y1, y2)
    print('Part 1:', val1)

    val2 = part2(x1, x2, y1, y2, vy_max)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
