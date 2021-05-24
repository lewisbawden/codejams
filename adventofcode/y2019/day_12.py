import aoc
import time
import re
import numpy as np

re_moon = re.compile("<x=(-?\d*), y=(-?\d*), z=(-?\d*)>")


def day_12_part_1(data, nums):
    orbits = Orbits(data)
    orbits.calculate_motion(nums)
    return orbits.total_energy


class Moon:
    def __init__(self, x, y, z):
        self.pos = [x, y, z]
        self.vel = [0, 0, 0]
        self.kin = 0
        self.pot = 0
        self.energy = 0

    def update_position(self, i):
        self.pos[i] += self.vel[i]

    def update_energies(self):
        self.pot = sum([abs(p) for p in self.pos])
        self.kin = sum([abs(v) for v in self.vel])
        self.energy = self.pot * self.kin


class Orbits:
    def __init__(self, moons):
        self.moons = moons
        self.num_moons = len(moons)
        self.total_energy = 0
        self.initial_keys = [self.update_key(0), self.update_key(1), self.update_key(2)]

    def evaluate_velocity(self, i, j, coord):
        if self.moons[i].pos[coord] == self.moons[j].pos[coord]:
            return
        elif self.moons[i].pos[coord] < self.moons[j].pos[coord]:
            self.moons[i].vel[coord] += 1
            self.moons[j].vel[coord] -= 1
        else:
            self.moons[i].vel[coord] -= 1
            self.moons[j].vel[coord] += 1

    def calc_velocity(self, coord):
        for i in range(self.num_moons - 1):
            for j in range(i + 1, self.num_moons):
                self.evaluate_velocity(i, j, coord)

    def calc_positions(self, coord):
        for moon in self.moons:
            moon.update_position(coord)

    def calc_energies(self):
        self.total_energy = 0
        for moon in self.moons:
            moon.update_energies()
            self.total_energy += moon.energy

    def update_key(self, coord=None):
        if coord is not None:
            self.key = "__".join([
                "_".join([str(m.pos[coord]) for m in self.moons]),
                "_".join([str(m.vel[coord]) for m in self.moons])])
            return self.key

    def calculate_motion(self, steps):
        for t in range(steps):
            [self.calc_velocity(i) for i in range(3)]
            [self.calc_positions(i) for i in range(3)]
            self.calc_energies()
        return self.calc_energies()

    def find_repeated_coord(self, coord):
        t = 0
        while True:
            t += 1
            self.calc_velocity(coord)
            self.calc_positions(coord)
            self.update_key(coord)
            if self.initial_keys[coord] == self.key:
                return t

    def find_original_repeated_state(self):
        x = self.find_repeated_coord(0)
        y = self.find_repeated_coord(1)
        z = self.find_repeated_coord(2)
        xy = np.lcm(x, y, dtype='longlong')
        xyz = np.lcm(xy, z, dtype='longlong')
        return xyz


def day_12_part_2(data):
    orbits = Orbits(data)
    return orbits.find_original_repeated_state()


def parse_data(data):
    moons = []
    for line in data:
        m = re_moon.match(line)
        moons.append(Moon(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return moons


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_12_data.txt")
    parsed = parse_data(data)
    print(day_12_part_2(parsed))

    print(time.time() - t0)