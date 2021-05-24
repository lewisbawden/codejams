import aoc
import time
from tqdm import tqdm
from itertools import cycle


def day_16_part_1(data, phases):
    t0 = time.time()
    sequencers = [get_fft_sequencer(n + 1) for n in range(len(data))]
    for p in tqdm(range(phases), total=phases):
        data = calc_fft_signal(data, sequencers)
    return data, "".join([str(d) for d in data[:8]])


def calc_fft_signal(data, sequencers):
    out = [0] * len(data)

    def calc_single_output(pos):
        fft_rep = cycle(sequencers[pos])
        next(fft_rep)
        return abs(sum(sig * next(fft_rep) for sig in data)) % 10

    return [calc_single_output(pos) for pos in range(len(out))]


def get_fft_sequencer(n):
    base = [0, 1, 0, -1]
    pattern = []
    for b in base:
        pattern.extend([b] * n)
    return pattern


def day_16_part_2(data, phases, reps):
    sig = data * reps
    out, _ = day_16_part_1(sig, phases)
    skip = int("".join([str(s) for s in out[:7]]))
    return "".join([str(s) for s in out[skip: skip + 8]])


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_16_data.txt")
    data = [int(c) for c in data[0]]
    # print(day_16_part_1(data, 100))
    print(day_16_part_2(data, 100, 10000))

    print(time.time() - t0)
