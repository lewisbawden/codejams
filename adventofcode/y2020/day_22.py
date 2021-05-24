from adventofcode.y2019 import aoc
import time


def day_22_part_1(decks):
    try:
        while True:
            p1, p2 = decks[True].pop(), decks[False].pop()
            winner = p1 > p2
            decks[winner] = sorted([p1, p2]) + decks[winner]
    except IndexError:
        return sum(x * y for x, y in zip(decks[winner], range(1, len(decks[winner]) + 1)))


def day_22_part_2(decks):
    winner, decks = combat(decks)
    return sum(x * y for x, y in zip(decks[winner], range(1, len(decks[winner]) + 1)))


def combat(decks):
    recursion_dict = {}
    try:
        while True:
            p1, p2 = decks[True].pop(), decks[False].pop()
            key = ",".join([str(d) for d in decks[True]]) + "," + ",".join([str(d) for d in decks[False]])
            recursion_dict.get(key, proceed)()
            if p1 <= len(decks[True]) and p2 <= len(decks[False]):
                winner = combat({True: decks[True][-p1:].copy(), False: decks[False][-p2:].copy()})[0]
                played = [p2, p1] if winner else [p1, p2]
            else:
                winner = p1 > p2
                played = sorted([p1, p2])
            decks[winner] = played + decks[winner]
            recursion_dict[key] = raise_recursion_error
    except RecursionError:
        return True, decks
    except IndexError:
        return winner, decks


def proceed():
    pass


def raise_recursion_error():
    raise RecursionError


def parse_cards(data):
    s = ",".join(data).replace("\n", "").split(",,")
    decks = {True: [*reversed([int(d) for d in s[0].split(",")[1:]])],
             False: [*reversed([int(d) for d in s[1].split(",")[1:]])]}
    return decks


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_22_data.txt")
    print(day_22_part_2(parse_cards(data)))

    print(time.time() - t0)