import sys


def part1(data):
    return sum(
         sum(1 for n in nums if len(n) in {2, 4, 3, 7})
         for _, nums in data
    )


def part2(data):

    def solve_single(combos, nums):
        combos = [frozenset(s) for s in combos]

        one = next(c for c in combos if len(c) == 2)
        seven = next(c for c in combos if len(c) == 3)
        four = next(c for c in combos if len(c) == 4)
        eight = next(c for c in combos if len(c) == 7)

        # group 1 consists of 0, 6, 9
        group1 = [c for c in combos if len(c) == 6]

        # a 9 contains a 4
        nine = next(c for c in group1 if four.issubset(c))
        group1.remove(nine)

        # group 2 consists of 2, 3, 5
        group2 = [c for c in combos if len(c) == 5]

        # 3 is the only member of group two without a "1"
        three = next(c for c in group2 if one.issubset(c))
        group2.remove(three)

        # 5 is contained within 9
        five = next(c for c in group2 if c.issubset(nine))
        group2.remove(five)

        # 2 remains from group 2
        two, = group2

        # 6 contains 5
        six = next(c for c in group1 if five.issubset(c) and c != nine)
        group1.remove(six)

        # 0 remains from group 1
        zero, = group1

        combo_to_num = {
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
            six: 6,
            seven: 7,
            eight: 8,
            nine: 9,
            zero: 0,
        }

        res = [combo_to_num[frozenset(num)] for num in nums]
        return int(''.join(str(n) for n in res))

    nums = [solve_single(*d) for d in data]
    return sum(nums)


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.readlines()

    data = []
    for line in content:
        patterns, nums = line.split(' | ')
        patterns = patterns.strip().split(' ')
        nums = nums.strip().split(' ')
        data.append((patterns, nums))

    val1 = part1(data)
    print('Part 1:', val1)

    val2 = part2(data)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
