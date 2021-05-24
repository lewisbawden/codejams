import aoc
import aoc_opcode
import time


def day_5_part_1(data):
    aoc_opcode.run_opcode(5, data)
    return False


def day_5_part_2(data):

    return None


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_5_data.txt")
    parsed = [int(s) for s in data[0].split(",")]
    print(day_5_part_1(parsed))

    print(time.time() - t0)