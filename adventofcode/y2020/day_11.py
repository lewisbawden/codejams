from adventofcode.y2019 import aoc
import time
import numpy as np


def day_11_part_1(data):
    prev_state = 0*data
    seats, floor = get_seats_floor(data)
    while np.sum(prev_state - data) != 0:
        prev_state = data.copy()
        data = next_state(data, seats, floor)
    return np.sum(data).real


def get_seats_floor(data):
    floor_to_seats = np.vectorize(lambda x: 0 ** x)
    seats = floor_to_seats(np.imag((data - np.conjugate(data)) / 2))
    floor = floor_to_seats(seats)
    return seats, floor


def seat_rules(occupied_neighoburs, seat_state):
    if seat_state == 0 and occupied_neighoburs == 0:
        return 1
    if seat_state == 1 and occupied_neighoburs >= 4:
        return 0
    return seat_state


def next_state(data, seats, floor):
    pad = np.zeros(shape=(data.shape[0] + 4, data.shape[1] + 4), dtype=complex)
    for i in range(0, 3):
        for j in range(0, 3):
            pad[1 + i: i - 3, 1 + j: j - 3] = np.add(pad[1 + i: i - 3, 1 + j: j - 3], data)

    num_occ_neighbours = np.array(np.real(pad[2:-2, 2:-2]-data), dtype=complex)
    apply_seat_rules = np.vectorize(seat_rules)
    after_seat_rules = apply_seat_rules(np.real(num_occ_neighbours), np.real(data))

    data = (after_seat_rules*seats) + np.complex(0, 1)*floor
    return data


def print_output(data):
    seat_conv = np.vectorize(lambda x: {1:"#", 0:"L", 1j:"."}[x])
    print("\n", seat_conv(data))


def day_11_part_2(data):
    prev_state = data * 0
    print_output(data)

    seats, floor = get_seats_floor(data)

    while np.sum(prev_state - data) != 0:
        prev_state = data.copy()
        data = next_state_new_rules(data, seats, floor)
    return np.real(data).sum()


def next_state_new_rules(data, seats, floor):
    after_seat_rules = data * 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            new_state_ij = search_directions(data, i, j)
            after_seat_rules[i,j] = new_state_ij

    data = (after_seat_rules * seats) + np.complex(0, 1) * floor
    return data


def search_directions(data, i, j):
    neighbours = 0
    searched = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            neighbours += search_one_direction(data, i, j, di, dj)
            searched += 1
            left_to_search = 8 - searched
            if data[i,j].real == 0 and neighbours > 0:
                return data[i,j]
            if data[i,j].real == 1 and left_to_search < 5 - neighbours:
                return data[i,j]
            if data[i,j].real == 1 and neighbours > 4:
                return 0
    return 1


def search_one_direction(data, i, j, di, dj):
    i += di
    j += dj
    if i < 0 or j < 0:
        return 0

    try:
        while data[i, j].imag > 0:
            i += di
            j += dj
            if i < 0 or j < 0:
                return 0
        return data[i, j].real
    except IndexError:
        return 0


def parse_seats(data):
    seats = []
    for line in data:
        row = []
        for s in line:
            if s == "L":
                row.append(complex(0, 0))
            elif s == ".":
                row.append(complex(0, 1))
            elif s == "#":
                row.append(complex(1, 0))
        seats.append(row)
    return np.array(seats, dtype=complex)


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_11_data.txt")
    parsed = parse_seats(data)
    print(day_11_part_2(parsed))

    print(time.time() - t0)
