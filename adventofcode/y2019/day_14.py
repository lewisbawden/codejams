import aoc
import time
import numpy as np


def day_14_part_1(data):
    return get_required_ore_helper("FUEL", 1, data)


def get_required_ore_helper(ing, n, data):
    base_chems, surplus = get_required_chems(ing, n, data, chems=dict(), surplus=dict())
    return get_required_ore(base_chems, data)


def get_required_chems(name, need, data, chems=dict(), surplus={}):
    r = data[name]

    multiples = max(0, np.ceil((need - surplus.get(name, 0)) / r.yield_out))
    bonus = multiples * r.yield_out - need

    surplus[name] = bonus + surplus.get(name, 0)

    for n, chem in zip(r.yield_in, r.chems_in):
        if chem == "ORE":
            chems[name] = need + chems.get(name, 0)
        else:
            chems, surplus = get_required_chems(chem, (n * multiples), data, chems, surplus)
    return chems, surplus


def get_required_ore(chems, data):
    total = 0
    for chem, needed in chems.items():
        total += (np.ceil(needed / data[chem].yield_out) * data[chem].yield_in[0])
    return total


def day_14_part_2(data):
    total_ore = 1000000000000
    prev_fuel = 0

    first_guess = 1
    req_ore = 0
    while req_ore < total_ore:
        req_ore = get_required_ore_helper("FUEL", int(first_guess), data)
        first_guess *= 100
    fuel = first_guess

    while True:
        req_ore = get_required_ore_helper("FUEL", int(fuel), data)
        print(fuel, "==>", req_ore, "==>", req_ore < total_ore)
        diff = round(abs(fuel - prev_fuel) / 2)
        prev_fuel = fuel
        if req_ore > total_ore:
            fuel -= max(diff, 1)
        else:
            fuel += diff
            if diff == 0:
                break
    return fuel


class Reaction:
    def __init__(self, line):
        self.parse_reaction(line)

    def parse_reaction(self, line):
        reaction = line.replace(",", "").rstrip("\n").split("=>")
        self.yield_out, self.chem_out = reaction[1].split()
        self.yield_out = int(self.yield_out)
        ingredients = reaction[0].split()
        self.chems_in = [ing for i, ing in enumerate(ingredients) if i % 2 == 1]
        self.yield_in = [int(ing) for i, ing in enumerate(ingredients) if i % 2 == 0]


def parse_input(data):
    reactions = {}
    for line in data:
        r = Reaction(line)
        reactions[r.chem_out] = r
    return reactions


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_14_data.txt")
    r = parse_input(data)
    print(day_14_part_2(r))

    print(time.time() - t0)
