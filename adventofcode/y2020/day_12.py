from adventofcode.y2019 import aoc
import time
import numpy as np


def day_12_part_1(data):
    ship = np.zeros(2)
    theta = 0
    bearing = np.array([np.cos(theta), np.sin(theta)])
    sign = {"L": 1, "R": -1}
    actions = {"N": np.array([0, 1]), "S": np.array([0, -1]), "E": np.array([1, 0]),
               "W": np.array([-1, 0]), "F": bearing}
    for cmd in data:
        action, value = cmd[0], int(cmd[1:-1])
        if action in "LR":
            theta += sign[action]*value
            rads = theta * np.pi / 180
            bearing = np.array([np.round(np.cos(rads)), np.round(np.sin(rads))])
        else:
            ship += actions[action] * value
        actions["F"] = bearing
    return round(sum((abs(ship))))


def day_12_part_2(data):
    ship = np.array([0.0, 0.0])
    waypoint = np.array([10.0, 1.0])
    sign = {"L": 1, "R": -1}
    actions = {"N": np.array([0, 1]), "S": np.array([0, -1]), "E": np.array([1, 0]),
               "W": np.array([-1, 0]), "F": waypoint}
    for cmd in data:
        action, value = cmd[0], int(cmd[1:-1])
        if action in "LR":
            rads = sign[action] * value * np.pi / 180
            waypoint = np.dot(np.array([
                [np.cos(rads), -np.sin(rads)],
                [np.sin(rads), np.cos(rads)]]), waypoint)
        elif action in "NEWS":
            waypoint += actions[action] * value
        elif action == "F":
            ship += actions[action] * value
        actions["F"] = waypoint
    return round(sum((abs(ship))))


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_12_data.txt")
    print(day_12_part_2(data))

    print(time.time() - t0)
