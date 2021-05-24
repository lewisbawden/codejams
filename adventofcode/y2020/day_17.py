import time
import numpy as np
import itertools as it


def day_17_part_1(data):
    ds = data.shape[0]
    space = np.zeros(shape=(ds, ds, ds))
    space[1, :, :] = np.array(data)

    for cycle in range(6):
        space = next_state_3d(space)
    return space.sum()


def cube_rules(occupied_neighoburs, cube_state):
    if cube_state == 0 and occupied_neighoburs == 3:
        return 1
    if cube_state == 1 and occupied_neighoburs not in [2, 3]:
        return 0
    return cube_state


def next_state_3d(space):
    dims = 3
    pad = np.zeros(shape=([s + dims for s in space.shape]))
    expanded_space = pad[1:-1, 1:-1, 1:-1].copy()
    expanded_space[1:-1, 1:-1, 1:-1] = space
    for i, j, k, in it.product(*[range(3) for dim in range(dims)]):
        pad[1 + i: i - 3, 1 + j: j - 3, 1 + k: k - 3] = np.add(
            pad[1 + i: i - 3, 1 + j: j - 3, 1 + k: k - 3], space)

    num_occ_neighbours = np.array(pad[1:-1, 1:-1, 1:-1] - expanded_space)
    apply_cube_rules = np.vectorize(cube_rules)
    return apply_cube_rules(num_occ_neighbours, expanded_space)


def next_state_4d(space):
    dims = 4
    pad = np.zeros(shape=([s + dims for s in space.shape]))
    expanded_space = pad[1:-1, 1:-1, 1:-1, 1:-1].copy()
    expanded_space[1:-1, 1:-1, 1:-1, 1:-1] = space
    for i, j, k, w in it.product(*[range(3) for dim in range(dims)]):
        pad[1 + i: i - 3, 1 + j: j - 3, 1 + k: k - 3, 1 + w: w - 3] = np.add(
            pad[1 + i: i - 3, 1 + j: j - 3, 1 + k: k - 3, 1 + w: w - 3], space)

    num_occ_neighbours = np.array(pad[1:-1, 1:-1, 1:-1, 1:-1] - expanded_space)
    apply_cube_rules = np.vectorize(cube_rules)
    return apply_cube_rules(num_occ_neighbours, expanded_space)


def day_17_part_2(data):
    ds = data.shape[0]
    space = np.zeros(shape=(ds, ds, ds, ds))
    space[1, :, :, 1] = np.array(data)

    for cycle in range(6):
        space = next_state_4d(space)
    return space.sum()


def parse_cubes(data):
    cubes = []
    for line in data:
        row = []
        for c in line:
            if c == ".":
                row.append(0)
            elif c == "#":
                row.append(1)
        cubes.append(row)
    return np.array(cubes)


def input_data(req):
    test = """.#.
    ..#
    ###""".split("\n")

    puzzle = """####...#
    ......##
    ####..##
    ##......
    ..##.##.
    #.##...#
    ....##.#
    .##.#.#.""".split("\n")
    if req == 0:
        return test
    else:
        return puzzle


if __name__ == "__main__":
    t0 = time.time()

    data = parse_cubes(input_data(1))
    print(day_17_part_2(data))

    print(time.time() - t0)
