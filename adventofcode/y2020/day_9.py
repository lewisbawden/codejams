from adventofcode.y2019 import aoc
import time


def day_9_part_1(data, preamble=25):
    for idx, args in enumerate(yield_slices(data, preamble)):
        if not valid_number(args, preamble):
            return args, idx + preamble
    return None


def day_9_part_2(data):
    args, target_idx = day_9_part_1(data)
    target = args[1]
    for i in range(target_idx - 1, -1, -1):
        total = 0
        j = 0
        while total < target:
            total += data[i - j]
            j += 1
        if total == target:
            return data[i - j + 1: i + 1], min(data[i - j + 1: i + 1]) + max(data[i - j + 1: i + 1])
    return None


def yield_slices(data, preamble):
    i = 0
    while i < len(data) - preamble:
        yield data[i: preamble + i], data[preamble + i]
        i += 1
    raise StopIteration


def valid_number(slice_in, preamble):
    for i in range(preamble):
        for j in range(i + 1, preamble):
            if slice_in[0][i] + slice_in[0][j] == slice_in[1]:
                return True
    return False


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_9_data.txt")
    parsed = [int(n) for n in data]
    print(day_9_part_2(parsed))

    print(time.time() - t0)
