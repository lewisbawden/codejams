from adventofcode.y2019 import aoc
import time
import operator as op

ops = {"+": op.add, "*": op.mul}


def day_18_part_1(data):
    return sum(evaluate_expression(line)[0] for line in map(cleaned, data))


def evaluate_expression(line, start=0):
    bracketed_total = next((s for s in line[start:] if s.isnumeric()))

    idx = start
    while idx < len(line) - 1:
        char = line[idx]
        if char == ")":
            break
        if char == "(":
            bracketed_total, idx = evaluate_expression(line, idx + 1)
        if line[idx] in ops.keys():
            larg = bracketed_total
            rarg = line[idx + 1]
            if rarg.isnumeric():
                bracketed_total = ops[line[idx]](int(larg), int(rarg))
            else:
                rarg, idx = evaluate_expression(line, idx + 2)
                bracketed_total = ops[char](int(larg), int(rarg))
        idx += 1
    return bracketed_total, idx


def add_brackets_everywhere(line, idx=0):
    while True:
        idx = line.find("+", idx)
        args = line[idx - 1: idx + 2]
        next_args = line[idx - 2: idx + 3]
        # no more pluses needing brackets
        if idx == -1:
            return line
        # no brackets needed - brackets already around this plus
        if f"({args})" == next_args:
            idx += 2
            continue
        # find place for bracket to the left if needed
        if line[idx-1].isnumeric():
            openbr_idx = idx - 1
        else:
            openbr_idx = get_openbr_loc(line, idx)
        # find place for bracket to right if needed
        if line[idx + 1].isnumeric():
            closebr_idx = idx + 2
        else:
            closebr_idx = get_closebr_loc(line, idx)
        line = line.replace(line[openbr_idx: closebr_idx], "({})".format(line[openbr_idx: closebr_idx]))
        idx += 2


def get_closebr_loc(line, idx):
    start = idx
    while True:
        loc = line.find(")", idx) + 1
        if line[start: loc].count("(") == line[start: loc].count(")"):
            return loc
        idx = loc


def get_openbr_loc(line, idx):
    start = idx
    while True:
        loc = line.rfind("(", 0, idx)
        if line[loc: start].count("(") == line[loc: start].count(")"):
            return loc
        idx = loc


def day_18_part_2(data):
    ans = []
    for line in map(cleaned_bracketed, data):
        ans.append(evaluate_expression(line)[0])
    return sum(ans)


def cleaned_bracketed(line):
    return add_brackets_everywhere(cleaned(line))


def cleaned(line):
    return line.replace("\n", "").replace(" ", "")


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_18_data.txt")
    print(day_18_part_2(data))

    print(time.time() - t0)
