import time
import aoc
import aoc_opcode as opc


def day_2_main_1(data, n, v):
    init = data.copy()

    data[1] = n
    data[2] = v

    data = opc.run_opcode(0, data)

    return data[0], init


def day_2_main_2(data, ans):
    for n in range(100):
        for v in range(100):
            guess, data = day_2_main_1(data, n, v)
            if guess == ans:
                return n, v, 100*n + v


def parse_data(data):
    return [int(m) for m in data[0].split(",")]


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data("day_2_data.txt")
    parsed = parse_data(data)

    # print(day_2_main_1(parsed, 12, 2))
    print(day_2_main_2(parsed, 19690720))

    print(time.time() - t0)
