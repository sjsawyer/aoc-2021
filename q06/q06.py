import sys
import functools


def part1(data, n_days):
    # since there is no interaction b/w the fish, we can solve for each
    # initial internal timer independently
    ic_to_total = {}
    for i in range(0, 6 + 1):
        fish = [i]
        for _ in range(n_days):
            for j in range(len(fish)):
                if fish[j] == 0:
                    fish[j] = 6
                    fish.append(8)
                else:
                    fish[j] -= 1
        ic_to_total[i] = len(fish)
    return sum(ic_to_total[d] for d in data)


def part2(data, n_days):

    @functools.lru_cache(maxsize=None)
    def num_fish_total(ic, days):
        total = 1

        # reset ic to 6
        days += (6 - ic)
        ic += (6 - ic)

        while days >= 7:
            days -= 7
            total += num_fish_total(8, days)
        return total

    return sum(num_fish_total(d, n_days) for d in data)


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().split(',')

    data = [int(n) for n in content]

    val1 = part1(data, 80)
    print('Part 1:', val1)

    val2 = part2(data, 256)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
