import time
import aoc

_LDRU = {"L": 0, "R": 0, "U": 1, "D": 1}
_SIGN = {"L": -1, "R": 1, "U": 1, "D": -1}


def day_3_main_1(data):
    sc1 = get_wire_path(data[0])
    sc2 = get_wire_path(data[1])

    j = {x: {} for x, y in sc1}
    for x, y in sc1:
        j[x][y] = 0

    intersections = []
    min_d = 1e100
    for x, y in sc2:
        try:
            j[x][y] += 1
            if abs(x) + abs(y) != 0:
                intersections.append([x, y])
                min_d = min(min_d, abs(x) + abs(y))
        except KeyError:
            continue

    return min_d, intersections, sc1, sc2


def get_wire_path(path_cmds):
    c = [[0, 0]]
    for p in path_cmds:
        for xy in calc_next_coords(c[-1], p):
            c.append(xy)
    return c


def calc_next_coords(old_xy, new_p):
    def coord(c):
        return _LDRU[c]

    def direction(c):
        return _SIGN[c]

    visited = []
    for i in range(1, int(new_p[1:]) + 1):
        new_xy = old_xy.copy()
        new_xy[coord(new_p[0])] = old_xy[coord(new_p[0])] + direction(new_p[0]) * int(i)
        visited.append(new_xy)
    return visited


def day_3_main_2(data):
    min_d, intersections, sc1, sc2 = day_3_main_1(data)
    print(intersections)

    shortest = 1e100
    for x, y in intersections:
        step1 = get_steps_from_intersection(x, y, sc1)
        step2 = get_steps_from_intersection(x, y, sc2)

        print(x, y, step1, step2, step1 + step2)
        shortest = min(shortest, step1 + step2)
    return shortest


def get_steps_from_intersection(x, y, sc):
    for i, (xi, yi) in enumerate(sc):
        if xi == x and yi == y:
            return i


def parse_data(data):
    return [s.split(",") for s in data]


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data("day_3_data.txt")
    parsed = parse_data(data)

    print(day_3_main_1(parsed))
    print(day_3_main_2(parsed))

    print(time.time() - t0)
