import time
import sys
from tqdm import tqdm
from numpy.random import randint
from functools import lru_cache


def next_id():
    i = 0
    while True:
        yield i
        i += 1
id_gen = next_id()


class Item(object):
    def __init__(self, w, v):
        self.weight = w
        self.value = v
        self.id = next(id_gen)
        self.hash = "-{}".format(self.id)


def timed(fn):
    def wrap(*args, **kwargs):
        t0 = time.time()
        out = fn(*args, **kwargs)
        tf = time.time()
        print("Duration {}: {}".format(fn.__name__, tf - t0))
        return out
    return wrap


class KnapSacker(object):
    def __init__(self, items, name):
        self.name = name
        self.items = items  # sorted(items, key=lambda i: i.value / i.weight)
        self.len_items = len(self.items)
        self.knapsack = list()  # [False] * self.num_items
        self.cache = dict()

    @property
    def num_items(self):
        return len(self.items)

    @timed
    def solve(self, max_items, max_weight, mode=0):
        print(self.name)
        if mode == 0:
            try:
                sol, items = self.solve_recursive(max_items, max_weight)
            except RecursionError:
                print("RecursionError")
                return None
        elif mode == 1:
            for i in tqdm(range(self.len_items - 1, -1, -1), total=self.len_items):
                sol, items = self.solve_cached(max_items, max_weight, i)
                self.cache[(max_items, max_weight, i)] = {"output": (int(sol), items), "visited": 0}

        for p, i in enumerate(self.items):
            if i in items:
                self.knapsack.append(True)
                print("Item {}: Value {}: Weight {}:".format(p, i.value, i.weight))
            else:
                self.knapsack.append(False)
        return sol

    def solve_cached(self, max_items, max_weight, item_pos=0, best_items=None):
        if best_items is None:
            best_items = set()
        if max_items <= 0 or max_weight <= 0 or item_pos >= self.len_items:
            return int(0), set()

        out = self.cache.get((max_items, max_weight, item_pos), None)
        if out is not None:
            self.cache[(max_items, max_weight, item_pos)]["visited"] += 1
            return out["output"]

        item = self.items[item_pos]
        leave, best_items_leave = self.solve_cached(max_items, max_weight, item_pos + 1, best_items)

        if item.weight > max_weight:
            self.cache[(max_items, max_weight, item_pos)] = {"output": (int(leave), best_items_leave), "visited": 0}
            return leave, best_items_leave

        take, best_items_take = self.solve_cached(max_items - 1, max_weight - item.weight, item_pos + 1, best_items)
        take += item.value

        if take > leave:
            best_items_take.add(item)
            self.cache[(max_items, max_weight, item_pos)] = {"output": (int(take), best_items_take), "visited": 0}
            return take, best_items_take
        else:
            self.cache[(max_items, max_weight, item_pos)] = {"output": (int(leave), best_items_leave), "visited": 0}
            return leave, best_items_leave

    def solve_recursive(self, max_items, max_weight, item_pos=0, best_items=None):
        if max_items <= 0 or max_weight <= 0 or item_pos >= len(self.items):
            return 0, []

        item = self.items[item_pos]
        leave, best_items_leave = self.solve_recursive(max_items, max_weight, item_pos + 1, best_items)

        if item.weight > max_weight:
            return leave, best_items_leave

        take, best_items_take = self.solve_recursive(max_items - 1, max_weight - item.weight, item_pos + 1, best_items)
        take += item.value

        if take > leave:
            best_items_take.append(item)
            return take, best_items_take
        else:
            return leave, best_items_leave

    def show_knapsack(self):
        tv, tw, ti = 0, 0, 0
        for p, (i, take) in enumerate(zip(self.items, self.knapsack)):
            if take:
                tv += i.value
                tw += i.weight
                ti += 1
                print("Item no. {}: Take: {}, value: {}, weight: {}".format(p, take, i.value, i.weight))
        print("Total items: {}\nTotal value: {}\nTotal weight: {}".format(ti, tv, tw))


def get_items(argmin, argmax, num):
    values = randint(argmin, argmax, num)
    weights = randint(argmin, argmax, num)
    # values = [int(i) for i in "9 2 1 3 9 4 8 8 2 8 5 8 9 7 7 4 3 4 4 8".split()]
    # weights = [int(i) for i in "3 7 6 4 7 4 5 4 6 2 2 8 9 4 6 3 8 7 3 2".split()]
    # values = [10, 40, 30, 50]
    # weights = [5, 4, 6, 3]
    items = []
    for w, v in zip(weights, values):
        items.append(Item(w, v))
    return items


def main():
    argmin, argmax, num = 10, 100, 500
    items = get_items(argmin, argmax, num)

    max_items = num // 4
    max_weight = (argmax // 3) * max_items

    # k = KnapSacker(items, "mode0")
    # sol = k.solve(max_items, max_weight, mode=0)
    # if sol is not None:
    #     print("Output: {} for max weight: {}, max items: {}".format(sol, max_weight, max_items))
    #     k.show_knapsack()

    k2 = KnapSacker(items, "mode1")
    sol = k2.solve(max_items, max_weight, mode=1)
    print("Output: {} for max weight: {}, max items: {}".format(sol, max_weight, max_items))
    k2.show_knapsack()


if __name__ == "__main__":
    a = int()
    main()
