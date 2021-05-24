import time


def day_6_part_1(data):
    return sum(len(set(g.replace("\n", ""))) for g in "".join(data).split("\n\n"))


def day_6_part_2(data):
    groups = "".join(data).split("\n\n")
    total = 0
    for g in groups:
        req_count = g.count("\n") + 1
        g_nonewline = g.replace("\n", "")
        ans = set(g_nonewline)
        for a in ans:
            if g_nonewline.count(a) == req_count:
                total += 1
    return total


def load_data(fstr):
    with open(fstr, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    t0 = time.time()

    data = load_data(r"day_6_data.txt")
    print(day_6_part_2(data))

    print(time.time() - t0)
