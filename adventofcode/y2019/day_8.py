import aoc
import time
import numpy as np
from itertools import product
import matplotlib.pyplot as plt


def day_8_part_1(data):
    layers, rows, cols = data.shape
    zero_layer = 0
    layer_size = rows * cols
    num_zeros = layer_size
    for layer in range(layers):
        zeros = layer_size - np.count_nonzero(data[layer, :, :])
        if zeros < num_zeros:
            num_zeros = zeros
            zero_layer = data[layer, :, :]
    ones = len(np.extract(zero_layer == 1, zero_layer))
    twos = len(np.extract(zero_layer == 2, zero_layer))

    return ones * twos


def day_8_part_2(data):
    layers, rows, cols = data.shape
    image = np.ones((rows, cols)) * 2
    for r, c in product(range(rows), range(cols)):
        l = 0
        while data[l, r, c] == 2:
            l += 1
        image[r, c] = data[l, r, c]
    plt.imshow(image)
    plt.show()
    return image


def parse_data(data, w, h):
    layers = int(len(data[0]) / (w * h))
    arr = np.array([int(s) for s in data[0]])
    arr = np.reshape(arr, (layers, h, w), order='C')
    return arr


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_8_data.txt")
    parsed = parse_data(data, 25, 6)
    print(day_8_part_2(parsed))

    print(time.time() - t0)
