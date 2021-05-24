from adventofcode.y2019 import aoc
import time


def day_15_part_1(data, upto):
    rr = {int(n): ElfNum(i + 1) for i, n in enumerate(data)}

    spoken_last_turn = int(data[-1])
    for turn in range(len(data) + 1, upto + 1):
        spoken_this_turn = rr[spoken_last_turn].speak()
        try:
            rr[spoken_this_turn].update_spoken(turn)
        except KeyError:
            rr[spoken_this_turn] = ElfNum(turn)
        spoken_last_turn = spoken_this_turn

    return spoken_last_turn


class ElfNum:
    def __init__(self, first_spoken):
        self.last_spoke = first_spoken
        self.prev_last_spoke = first_spoken

    def speak(self):
        return self.last_spoke - self.prev_last_spoke

    def update_spoken(self, turn):
        self.prev_last_spoke = self.last_spoke
        self.last_spoke = turn


def day_15_part_2(data, upto):
    return day_15_part_1(data, upto)


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_15_data.txt")
    data = [d.split() for d in data]
    for inp in data:
        if inp[0] == "test":
            ans = day_15_part_1(inp[1:-1], 2020)
            print(ans == int(inp[-1]), ans, inp[-1])

    print(day_15_part_2(data[-1], 30000000))

    print(time.time() - t0)
