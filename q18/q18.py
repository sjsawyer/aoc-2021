import sys
from functools import reduce
import heapq


class SnailNumber:
    """
    A snail number is a pair of two elements, where each element is either
    a regular number or another `SnailNumber`
    """
    def __init__(self, left=None, right=None, parent=None, value=None):
        self.left = left
        self.right = right
        self.value = value
        self.parent = parent

    @classmethod
    def from_list(cls, l, parent=None):
        sn = cls()

        if isinstance(l[0], list):
            left = cls.from_list(l[0], parent=sn)
        else:
            left = SnailNumber(value=l[0], parent=sn)

        if isinstance(l[1], list):
            right = cls.from_list(l[1], parent=sn)
        else:
            right = SnailNumber(value=l[1], parent=sn)

        sn.left = left
        sn.right= right
        sn.parent = parent

        return sn

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return '[' + repr(self.left) + ',' + repr(self.right) + ']'

    def print_tree(self):
        n = self
        while n.parent is not None:
            n = n.parent
        print(repr(n))


def magnitude(sn):
    if sn.value is not None:
        return sn.value
    return 3*magnitude(sn.left) + 2*magnitude(sn.right)


def get_next_left(sn, path):

    # first traverse up until we can go left again
    while sn.parent:
        parent = sn.parent
        if parent.left and parent.left != sn:
            sn = parent.left
            path = path[:-1] + 'l'
            break
        sn = sn.parent
        path = path[:-1]

    if not sn.parent:
        return None, None

    # now go all the way right
    while sn.right:
        sn = sn.right
        path += 'r'

    return sn, path


def get_next_right(sn, path):

    # first traverse up until we can go right again
    while sn.parent:
        parent = sn.parent
        if parent.right and parent.right != sn:
            sn = parent.right
            path = path[:-1] + 'r'
            break
        sn = sn.parent
        path = path[:-1]

    if not sn.parent:
        return None, None

    # now go all the way left
    while sn.left:
        sn = sn.left
        path += 'l'

    return sn, path


def heap_add(heap, key, num, contained):
    if key not in contained:
        if key[0] == 's' and 'e' + key[1:-1] in contained:
            # we are already exploding, don't split
            return
        heapq.heappush(heap, (key, num))
        contained.add(key)

def heap_pop(heap, contained):
    key, num = heapq.heappop(heap)
    contained.remove(key)
    return key, num


def explode(sn, path, todo, intodo):
    # add left to the next leftmost thing. to do this, keep ascending up
    # tree until we can go left again, then go left, and then keep
    # going right
    left_val = sn.left.value
    right_val = sn.right.value
    left, left_path = get_next_left(sn, path)
    right, right_path = get_next_right(sn, path)

    # update and split if necessary
    if left:
        left.value += left_val
        if left.value > 9:
            heap_add(todo, 's' + left_path, left, intodo)
    if right:
        #if right_path == 'rrrl':
        #    print('\nhere', right_path, right.value, '\n')
        right.value += right_val
        if right.value > 9:
            heap_add(todo, 's' + right_path, right, intodo)

    # replace ourselves in the tree
    new_sn = SnailNumber(value=0)
    parent = sn.parent
    if sn.parent.left == sn:
        sn.parent.left = new_sn
    else:
        sn.parent.right = new_sn
    new_sn.parent = parent


def split(sn, path, todo, intodo):
    # construct new
    left_val = sn.value // 2
    right_val = (sn.value + 1) // 2
    sn_new = SnailNumber.from_list([left_val, right_val])
    # replace old
    parent = sn.parent
    sn_new.parent = parent
    if parent.left == sn:
        parent.left = sn_new
    else:
        parent.right = sn_new

    if len(path) >= 4:
        # we need to explode what we just created
        heap_add(todo, 'e' + path, sn_new, intodo)
        # if we are exploding, then don't bother splitting
        return

    if left_val > 9:
        # need to split again
        heap_add(todo, 's' + path + 'l', sn_new.left, intodo)

    if right_val > 9:
        # need to split again
        heap_add(todo, 's' + path + 'r', sn_new.right, intodo)


def add_snail_numbers(sn1, sn2):
    # first construct the new number
    sn = SnailNumber(left=sn1, right=sn2)
    sn1.parent = sn
    sn2.parent = sn

    # a min heap with priority on explodes and left most nodes
    # sample keys and comparisons:
    #   'ellrl' < 'erlrl'
    #   'ellrl' < 'slrrl'
    #   'sl' < 'sr'
    todo = []
    # store keys in seen so we don't repeat
    intodo = set()

    def populate(number, depth, path):
        if number is None:
            return
        if depth == 4 and number.value is None:
            # explode this number
            heap_add(todo, 'e' + path, number, intodo)
        elif number.value is not None and number.value > 9:
            # split this number
            heap_add(todo, 's' + path, number, intodo)

        populate(number.left, depth + 1, path + 'l')
        populate(number.right, depth + 1, path + 'r')

    # get the initial tasks to do
    populate(sn, 0, '')

    # now do them
    j = 0
    print("reducing:", sn)
    while todo:
        #print(j)
        print(todo)
        sn.print_tree()
        key, number = heap_pop(todo, intodo)
        #print(len(todo))
        task, path = key[0], key[1:]
        if task == 'e':
            explode(number, path, todo, intodo)
            print("exploded:", sn)
        elif task == 's':
            split(number, path, todo, intodo)
            print("split:   ", sn)
        else:
            raise Exception('oh shittt')

    print(sn)
    return sn



def main(input_file):
    with open(input_file, 'r') as f:
        content = f.read().splitlines()

    numbers = [eval(s) for s in content]
    snail_numbers = [SnailNumber.from_list(l) for l in numbers]
    res = reduce(lambda x, y: add_snail_numbers(x, y), snail_numbers)
    mag = magnitude(res)
    print(mag)
    #print(res)


    #assert (
    #    add_snail_numbers(snail_numbers[0], snail_numbers[1]) ==
    #    SnailNumber.from_list([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    #)




if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
