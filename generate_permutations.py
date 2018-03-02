import itertools
import string
import sys


def generate(str_rack, wildcard):
    wildcard = bool(wildcard)
    racks = []
    rack = sorted(list(str_rack))[1:]

    if wildcard == 'True':
        for c in string.ascii_lowercase:
            new_rack = rack + ['?' + c]
            racks.append(new_rack)
    else:
        racks.append(rack)

    s = set()
    for r in racks:
        for i in range(1, len(r) + 1):
            for p in itertools.permutations(r, i):
                s.add(''.join(p))

    with open('./resources/permutations.txt', mode='w') as f:
        for p in s:
            f.write(p + '\n')


if __name__ == '__main__':
    args = sys.argv[1:]
    generate(*args)
