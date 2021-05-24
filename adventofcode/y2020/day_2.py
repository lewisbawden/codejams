import time
import numpy as np


def day_2_part_1(data):
    valid = 0
    for idx, data_i in enumerate(data):
        llim, ulim, key, password = data_i
        occurences = password.count(key)
        if occurences >= llim and occurences <= ulim:
            valid += 1
    print(valid)


def day_2_part_2(data):
    cond1 = np.array([password[llim - 1] == key for llim, ulim, key, password in data])
    cond2 = np.array([password[ulim - 1] == key for llim, ulim, key, password in data])

    valid = np.logical_xor(cond1, cond2)
    print(valid.sum())


def parse_line(line):
    a, b, c, d = line.replace("-", " ").replace(":", "").split()
    return int(a), int(b), c, d


if __name__ == "__main__":
    t0 = time.time()

    with open("day_2_data.txt", "r") as f:
        lines = f.readlines()
    data = [parse_line(l) for l in lines]

    day_2_part_2(data)

    print(time.time() - t0)