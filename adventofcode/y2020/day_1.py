import numpy as np
import time


def day_1_part_1(data):
    i, j = get_two_indices(sorted(data))
    print(i, j, i*j)


def day_1_part_2(data):
    i, j, k = get_three_indices(sorted(data))
    print(i, j, k, i*j*k)


def get_two_indices(data, total=2020):
    for i in data:
        for j in data:
            if i+j == total:
                return i, j


def get_three_indices(data, total=2020):
    for i in data:
        for j in data:
            for k in data:
                sum_ijk = i + j + k
                if sum_ijk > total:
                    break
                if sum_ijk == total:
                    return i, j, k


if __name__ == "__main__":
    expenses = np.loadtxt(r"day_1_data.txt")

    t0 = time.time()
    day_1_part_2(expenses)
    print(time.time() - t0)

