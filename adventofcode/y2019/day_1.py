import aoc
import numpy as np


def day_1_main_1(data):
    t = 0
    for m in data:
        t += get_fuel(m)
    return t


def day_1_main_2(data):
    t = 0
    for m in data:
        t += get_fuel_recr(m)
    return t


def get_fuel(mass):
    return max(np.floor(int(mass)/3) - 2, 0)


def get_fuel_recr(mass, total_fuel=0):
    if int(mass) <= 0:
        return total_fuel
    total_fuel += get_fuel(mass)
    return get_fuel_recr(get_fuel(mass), total_fuel)


if __name__ == "__main__":
    data = aoc.load_data("day_1_data.txt")

    print(day_1_main_1(data))
    print(day_1_main_2(data))
