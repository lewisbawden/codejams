import aoc
import time
from aoc_opcode import IntCode
import numpy as np
import matplotlib.pyplot as plt


def day_11_part_1(data):
    robot = Robot(data)
    robot.paint_tiles()
    return len(robot.painted)


class Robot:
    def __init__(self, data):
        self.intcode = IntCode(data)
        self.x = 0
        self.y = 0
        self.dir = (0, 1)
        self.rot = [[[0, -1], [1, 0]], [[0, 1], [-1, 0]]]
        self.painted = {}
        self.image = None

    def get_painted(self):
        try:
            t = self.painted[(self.x, self.y)]
        except KeyError:
            t = 0
        return t

    def paint_tiles(self):
        ec = False
        while not ec:
            tile = self.get_painted()
            ec, out = self.intcode.run_opcode(tile)
            self.painted[(self.x, self.y)] = out[0]
            self.dir = np.dot(self.rot[out[1]], self.dir)
            self.x += self.dir[0]
            self.y += self.dir[1]


def day_11_part_2(data):
    robot = Robot(data)
    robot.painted[(0,0)] = 1
    robot.paint_tiles()
    fig, ax = plt.subplots(figsize=(7, 7))
    plt.scatter([x for x, y in robot.painted],
                [y for x, y in robot.painted],
                [20 for i in range(len(robot.painted))],
                [c for c in robot.painted.values()],
                marker='s')
    ax.set_aspect('equal')
    plt.show()
    return None


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_11_data.txt")
    print(day_11_part_2(data))

    print(time.time() - t0)
