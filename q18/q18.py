import sys


class SnailNumber:
    """
    A snail number is a pair of two elements, where each element is either
    a regular number or another `SnailNumber`
    """
    def __init__(self, left=None, right=None, parent=None, value=None, signature=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent
        self.signature = signature

    @classmethod
    def from_list(cls, l, parent=None, signature = ''):
        sn = cls()

        leftsig = signature + 'l'
        if isinstance(l[0], list):
            left = cls.from_list(l[0], parent=sn, signature=leftsig)
        else:
            left = SnailNumber(value=l[0], signature=leftsig)

        rightsig = signature + 'r'
        if isinstance(l[1], list):
            right = cls.from_list(l[1], parent=sn, signature=rightsig)
        else:
            right = SnailNumber(value=l[1], signature=rightsig)

        sn.left = left
        sn.right= right
        sn.parent = parent
        sn.signature = signature

        return sn

    def __repr__(self):
        if self.value:
            return str(self.value)
        else:
            return '[' + repr(self.left) + ',' + repr(self.right) + ']'



def add_snail_numbers(sn1, sn2):
    # first construct the new number
    sn = SnailNumber(left=sn1, right=sn2)
    sn1.parent = sn
    sn2.parent = sn

    # operations to perform:



def part1(data):
    pass


def part2(data):
    pass


def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().splitlines()

    numbers = [eval(s) for s in content]
    import pdb; pdb.set_trace()
    snail_numbers = [SnailNumber.from_list(l) for l in numbers]

    assert (
        add_snail_numbers(snail_numbers[0], snail_numbers[1]) ==
        SnailNumber.from_list([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    )


    #val1 = part1(numbers)
    #print('Part 1:', val1)

    #val2 = part2(content)
    #print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
