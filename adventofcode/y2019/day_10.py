import aoc
import time
import numpy as np
from itertools import product, cycle


def day_10_part_1(data):
    out = data.copy()
    max_astroids = -1
    best_base = (-1, -1)
    for i, j in product(range(data.shape[0]), range(data.shape[1])):
        out[i, j] = astroids_in_los(data, i, j)
        if out[i, j] > max_astroids:
            max_astroids = out[i, j]
            best_base = (j, i)
    return best_base, max_astroids


class Astroid:
    def __init__(self, i, j, base_i, base_j):
        self.i = i
        self.j = j
        self.r = np.sqrt((base_i - i) ** 2 + (base_j - j) ** 2)
        self.theta = np.arctan2(base_j - j, base_i - i) * -180 / np.pi
        if self.theta < 0:
            self.theta += 360
        self.destroyed = base_i == i and base_j == j


def astroids_in_los(data, r, c):
    if data[r, c] == 1:
        return get_astroids_in_los(data, r, c)
    else:
        return -1


def get_astroids_in_los(data, r, c):
    rows, cols = data.shape
    top, bottom, left, right = r + 1, rows - r, c + 1, cols - c

    astroids = 0
    if any(data[: r, c] == 1): astroids += 1
    if any(data[r + 1:, c] == 1): astroids += 1
    if any(data[r, : c] == 1): astroids += 1
    if any(data[r, c + 1:] == 1): astroids += 1

    for i, j in product(range(1, top), range(1, left)):
        astroids += check_single_los(data, r, -i, c, -j, rows, cols)

    for i, j in product(range(1, top), range(1, right)):
        astroids += check_single_los(data, r, -i, c, j, rows, cols)

    for i, j in product(range(1, bottom), range(1, left)):
        astroids += check_single_los(data, r, i, c, -j, rows, cols)

    for i, j in product(range(1, bottom), range(1, right)):
        astroids += check_single_los(data, r, i, c, j, rows, cols)

    return astroids


def check_single_los(data, r, i, c, j, rows, cols):
    if np.gcd(abs(i), abs(j)) != 1:
        return 0

    n = 1
    ri, cj = r + i, c + j
    while valid_coords(ri, cj, rows, cols):
        if data[ri, cj] == 1:
            return 1
        n += 1
        ri, cj = r + n * i, c + n * j
    return 0


def valid_coords(ri, cj, rows, cols):
    if ri < 0 or cj < 0:
        return False
    elif ri > rows - 1 or cj > cols - 1:
        return False
    else:
        return True


def day_10_part_2(data):
    coords, total_astroids = ((11, 13), 227)
    base_j, base_i = coords
    astroids = [Astroid(i, j, base_i, base_j) for i, j in product(range(data.shape[0]), range(data.shape[1])) if data[i, j] == 1]
    astroids.sort(key=lambda a: (a.theta, a.r))

    target_angles = cycle(set(a.theta for a in astroids))
    destroyed = []
    try:
        while True:
            next_target = next(target_angles)
            target = next(a for a in astroids if a.theta == next_target and not a.destroyed)
            destroyed.append(target)
            target.destroyed = True
    except StopIteration:
        return destroyed[199].j * 100 + destroyed[199].i


def parse_lines(data):
    def parse_line(line):
        return line.replace(".", "0 ").replace("#", "1 ").split()
    return np.array([parse_line(line) for line in data], dtype=int)


if __name__ == "__main__":
    t0 = time.time()

    _data = aoc.load_data(r"day_10_data.txt")
    _parsed = parse_lines(_data)
    print(day_10_part_1(_parsed))
    print(day_10_part_2(_parsed))

    print(time.time() - t0)
