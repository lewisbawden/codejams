from adventofcode.y2019 import aoc
import time
from functools import lru_cache


def day_10_part_1(data):
    return get_differences(data)


def get_differences(soln):
    jolt_one_diffs = sum((1 for i, j in zip(soln[:-1], soln[1:]) if j - i == 1))
    jolt_three_diffs = sum((1 for i, j in zip(soln[:-1], soln[1:]) if j - i == 3))
    return jolt_one_diffs, jolt_three_diffs, jolt_one_diffs * jolt_three_diffs


def day_10_part_2():
    return get_valid_solutions()


@lru_cache()
def get_valid_solutions(root_idx=0, total=0):
    if root_idx == len(data) - 2:
        return 1

    valid_children = get_valid_children(root_idx)

    valid_children_solutions = 0
    for child_idx in valid_children:
        valid_children_solutions += get_valid_solutions(child_idx, total)

    return total + valid_children_solutions


def get_valid_children(root_idx):
    valid_children = []
    i = 1
    while data[root_idx + i] <= data[root_idx] + 3:
        valid_children.append(root_idx + i)
        i += 1
    return valid_children


if __name__ == "__main__":
    t0 = time.perf_counter()

    data = aoc.load_data(r"day_10_data.txt")
    data = sorted(int(x) for x in data)
    data = [0] + data + [data[-1] + 3]
    print(day_10_part_2())

    print(time.perf_counter() - t0)
