import time


def day_4(n1, n2, is_valid_fn):
    passwords = 0
    ns = [i for i in range(n1, n2 + 1)]
    ns_valid = map(is_valid_fn, ns)
    passwords = list(ns_valid).count(True)

    return passwords


def is_valid_p1(n):
    n_str = str(n)
    n_arr = [int(i) for i in str(n)]
    valid = False
    for i in range(1, 6):
        if n_arr[i] < n_arr[i - 1]:
            return False
        elif n_arr[i] == n_arr[i - 1]:
            valid = True
    return valid


def is_valid_p2(n):
    n_str = str(n)
    n_arr = [int(i) for i in str(n)]
    valid = False
    for i in range(1, 6):
        rep_str = str(n_arr[i])*3
        if n_arr[i] < n_arr[i - 1]:
            return False
        elif n_arr[i] == n_arr[i - 1] and rep_str not in n_str:
            valid = True
    return valid


if __name__ == "__main__":
    t0 = time.time()

    print(day_4(147981, 691423, is_valid_p1))
    print(day_4(147981, 691423, is_valid_p2))

    print(time.time() - t0)