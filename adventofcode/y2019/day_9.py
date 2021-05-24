import aoc
import time
from aoc_opcode import IntCode


def day_9_part_1(data):
    comp = IntCode(data)
    ec, outp = comp.run_opcode(1)
    return outp


def day_9_part_2(data):
    comp = IntCode(data)
    ec, outp = comp.run_opcode(2)
    return outp


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_9_data.txt")
    print(day_9_part_1(data))
    print(day_9_part_2(data))

    print(time.time() - t0)
