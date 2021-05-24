import aoc
import time


def day_6_part_1(data):
    orbits = get_planets(data)
    orbits['COM'].direct = 0
    orbits['COM'].indirect = 0

    def get_orbits(planet):
        for child in planet.children:
            orbits[child].direct = 1
            orbits[child].indirect = planet.indirect + planet.direct
            get_orbits(orbits[child])

    get_orbits(orbits['COM'])
    total = [orbits[planet].direct + orbits[planet].indirect for planet in orbits.keys()]

    return orbits, sum(total)


def get_planets(data):
    planets = {}
    for line in data:
        parent_name, child_name = line.strip("\n").split(")")
        try:
            planets[parent_name].children += [child_name]
        except KeyError:
            planets[parent_name] = Planet(name=parent_name, children=child_name)
        try:
            planets[child_name].parent = parent_name
        except KeyError:
            planets[child_name] = Planet(name=child_name, parent=parent_name)
    return planets


class Planet:
    def __init__(self, name, parent=None, children=None, direct=None, indirect=None):
        self.name = name
        self.parent = parent
        if children is not None:
            self.children = [children]
        else:
            self.children = []
        self.direct = direct
        self.indirect = indirect


def day_6_part_2(data):
    orbits, total = day_6_part_1(data)

    def orbit_chain(planet, chain=None):
        if chain is None:
            chain = set()
        if planet.name == 'COM':
            return chain
        chain.add(planet.parent)
        chain = orbit_chain(orbits[planet.parent], chain)
        return chain

    you_orbit_chain = orbit_chain(orbits['YOU'])
    san_orbit_chain = orbit_chain(orbits['SAN'])
    transfers = you_orbit_chain.symmetric_difference(san_orbit_chain)

    return len(transfers)


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_6_data.txt")
    print(day_6_part_1(data))
    print(day_6_part_2(data))

    print(time.time() - t0)
