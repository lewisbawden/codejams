import time
import numpy as np


def day_3_part_1(data, drow, dcol):
    row_idx = col_idx = 0
    max_rows, max_cols = data.shape
    trees = 0

    while row_idx < max_rows:
        trees += data[row_idx][col_idx % max_cols]
        row_idx += drow
        col_idx += dcol

    return trees


def day_3_part_2(data):
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]

    ans = np.longlong(1)
    for slope in slopes:
        trees = day_3_part_1(data, *slope)
        ans *= trees
        print(trees)

    print(ans)


def parse_lines(line):
    return line.replace(".", "0 ").replace("#", "1 ").split()


if __name__ == "__main__":
    t0 = time.time()

    with open("day_3_data.txt", "r") as f:
        lines = f.readlines()
    data = np.array([parse_lines(line) for line in lines], dtype=int)

    day_3_part_2(data)

    print(time.time() - t0)
