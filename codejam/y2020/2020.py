import sys
from itertools import permutations, cycle


def _gen_input():
    inp = """3
    3 6
    2 3"""
    for i in inp.split("\n"):
        yield i


_gen = iter(_gen_input())
def input():
    return next(_gen)



def p1():
    num_mats = int(input())

    for mi in range(num_mats):
        tr = 0
        nrows = int(input())
        reprows = 0
        cols = [set() for s in range(nrows)]
        for ri in range(nrows):
            vals = [int(v) for v in input().split()]
            tr += vals[ri]
            s = set(v for v in vals)
            reprows += (1 if len(s) != nrows else 0)
            for ci in range(nrows):
                cols[ci].add(vals[ci])
        repcols = sum(1 if len(cs) != nrows else 0 for cs in cols)
        print("Case #{}: {} {} {}".format(mi + 1, tr, reprows, repcols))


def p2():
    num_inps = int(input())
    for i in range(num_inps):
        row = input()
        out = place_brackets(row)
        print(f"Case #{i + 1}: {out}")


def get_b_type(n):
    if n > 0:
        return "("
    elif n < 0:
        return ")"
    else:
        return ""


def place_brackets(sv: str):
    i = 0
    out = "(" * int(sv[i]) + sv[i]
    for i in range(1, len(sv)):
        num = int(sv[i]) - int(sv[i - 1])
        b = get_b_type(num)
        out += (b * abs(num)) + sv[i]
    out += ")" * int(sv[i])
    return out


def p3():
    num_cases = int(input())
    nostr = "IMPOSSIBLE"
    cstr = "C"
    jstr = "J"
    for i in range(num_cases):
        num_acts = int(input())
        c, j = 0, 0
        tasks = [[act] + [int(a) for a in input().split()] for act in range(num_acts)]
        sorted_tasks = sorted(tasks, key=lambda t: t[1])
        out_arr = [None for t in range(num_acts)]
        for ia in range(num_acts):
            na, s, f = sorted_tasks[ia]
            if c <= s:
                c = f
                out_arr[na] = cstr
            elif j <= s:
                j = f
                out_arr[na] = jstr
            else:
                break
        if any(task is None for task in out_arr):
            out = nostr
        else:
            out = "".join(out_arr)
        print(f"Case #{i + 1}: {out}")


class Solver:
    def __init__(self):
        self.qs = 1
        self.case = 1
        self.num_tests, self.bsize = [int(i) for i in input().split()]
        self.print_debug(self.num_tests)

    @property
    def fluc_round(self):
        return self.qs % 10 == 1

    def print_debug(self, out, do_print=False):
        fmt_str = f" debug case {self.case + 1}, q {self.qs}: {out}"
        if do_print:
            print(fmt_str, file=sys.stderr)

    def rev_comp_convert(self, arr, do_rev, do_comp):
        if do_rev:
            self.print_debug(f"doing rev")
            arr.reverse()
        if do_comp:
            self.print_debug(f"doing comp")
            arr = [0 ** i for i in arr]
        return arr

    def solve(self):
        for test in range(self.num_tests):
            self.case = test
            self.key = self.get_key()
            self.print_debug(f"trying {self.key}")
            print(self.key)
            out = input()
            if out == "N":
                self.print_debug("failed")
                return 1
            elif out == "Y":
                self.print_debug(f"success")
                while self.qs % 10 != 1:
                    self.print_debug("judge resetting to 1st question:- skipping ahead")
                    self.qs += 1
        self.print_debug("all tests successful")
        return 0

    def get_key(self):
        self.key = [0 for i in range(self.bsize)]
        determined, past_halfway = False, False
        rev_id, comp_id = -1, -1
        pointer = 1
        while not determined or not past_halfway:
            if self.fluc_round:
                determined = self.solve_fluc_round(rev_id, comp_id)

            first, last = pointer, self.bsize - (pointer - 1)
            past_halfway = first > last

            for idx in (first, last):
                print(idx)
                out = int(input())
                self.key[idx - 1] = out
                self.print_debug(f"{pointer}, {idx}, {out}, {self.key}")
                self.qs += 1

            if comp_id < 0 and self.key[first - 1] == self.key[last - 1]:
                comp_id = first
            elif rev_id < 0 and self.key[first - 1] != self.key[last - 1]:
                rev_id = first

            if first == self.bsize:
                determined = True

            pointer += 1
        return "".join([str(i) for i in self.key])

    def solve_fluc_round(self, rev_id, comp_id):
        """
        rev:  if we expect 0 1: we could get
                0 1 -> (comp && rev) || nothing
                1 0 -> rev || comp
        comp: if we expect 0 0: we could get
                0 0 -> nothing || rev
                1 1 -> comp || (rev && comp)
            Options:
                r same, c same -> nothing
                r diff, c same -> rev
                r same, c diff -> rev && comp
                r diff, c diff -> comp
        """
        self.print_debug(f"Fluc. round: qs = {self.qs}")
        do_comp = False
        do_rev = False
        if comp_id > 0:
            print(comp_id)
            out = int(input())
            comp_same = out == self.key[comp_id - 1]
            self.print_debug(f"Check comp {comp_id}: got {out}, expected {self.key[comp_id - 1]}")
            do_comp = not comp_same
            self.print_debug(f"comp same {comp_same}")
        else:
            print(1)
            input()

        if rev_id > 0:
            print(rev_id)
            out = int(input())
            rev_same = out == self.key[rev_id - 1]
            self.print_debug(f"Check reverse {rev_id}: got {out}, expected {self.key[rev_id - 1]}")
            self.print_debug(f"rev same {rev_same}")

            if comp_id > 0:
                do_rev = comp_same != rev_same
            else:
                do_rev = not rev_same
                do_comp = False
        else:
            print(1)
            input()

        self.print_debug(f"do rev {do_rev}, do comp {do_comp}")
        self.key = self.rev_comp_convert(self.key, do_rev, do_comp)
        self.qs += 2
        return True

def p4():
    Solver().solve()


def p5():
    num_cases = int(input())
    for case in range(num_cases):
        n, k = [int(i) for i in input().split()]
        sol = make_mat(n, k)
        print_sol(case, sol)


def make_mat(n, k):
    out = []
    if k % n == 0:
        out = arith_mat(n, k)
    else:
        out = None
    return out


def perm_mat(n, k):
    nums = [i for i in range(1, n + 1)]
    rep_nums = cycle(permutations(nums))
    row = 0
    out = []
    while row < n:
        out.append([i for i in next(rep_nums)])
        row += 1
    return out


def arith_mat(n, k):
    nums = [i for i in range(1, n + 1)]
    rep_nums = cycle(nums)
    for i in range((k // n) - 1):
        next(rep_nums)
    row = 0
    out = []
    while row < n:
        out.append([next(rep_nums) for i in range(n)])
        for i in range(n - 1):
            next(rep_nums)
        row += 1
    return out


def print_sol(i, sol):
    if sol is None:
        print(f"Case #{i + 1}: IMPOSSIBLE")
    else:
        print(f"Case #{i + 1}: POSSIBLE")
        [print(" ".join([str(a) for a in row])) for row in sol]


if __name__ == "__main__":
    # p1()
    # p2()
    # p3()
    # p4()
    p5()