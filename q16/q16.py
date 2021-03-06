import sys
from functools import reduce

def char_to_bin(c):
    return "{0:04b}".format(int(c, 16))


def hex_to_bits(hex_string):
    return ''.join(char_to_bin(c) for c in hex_string)


def decode(hex_string):
    versions = []
    packet = hex_to_bits(hex_string)

    def process_packet(i):

        def read(n):
            nonlocal i
            res = int(packet[i:i+n], 2)
            i += n
            return res

        version = read(3)
        versions.append(version)

        type_id = read(3)
        if type_id == 4:
            literal = 0
            not_last = True
            while not_last:
                data = read(5)
                not_last = data & 0b10000
                literal = (literal << 4) | (data & 0b01111)
            return i, literal

        else:
            length_type_id = read(1)
            values = []
            if length_type_id == 0:
                total_len = read(15)
                j = i
                i += total_len
                while j < i:
                    j, val = process_packet(j)
                    values.append(val)
            else:
                num_packets = read(11)
                for _ in range(num_packets):
                    i, val = process_packet(i)
                    values.append(val)

            res = None
            if type_id == 0:
                res = sum(values)
            elif type_id == 1:
                res = reduce(lambda x,y: x*y, values)
            elif type_id == 2:
                res = min(values)
            elif type_id == 3:
                res = max(values)
            elif type_id == 5:
                res = int(values[0] > values[1])
            elif type_id == 6:
                res = int(values[0] < values[1])
            elif type_id == 7:
                res = int(values[0] == values[1])

            return i, res

    _, res = process_packet(0)
    return sum(versions), res


def main(input_file):
    with open(input_file, 'r') as f:
        hex_string = f.read().strip()

    val1, val2 = decode(hex_string)
    print('Part 1:', val1)
    print('Part 2:', val2)


if __name__ == '__main__':
    input_file = sys.argv[-1] if len(sys.argv) > 1 else 'input.txt'
    main(input_file)
