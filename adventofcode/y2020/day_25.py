import time


def day_25_part_1(card, door):
    subject_num = 7
    code_val = 20201227
    card_loop = get_loop_size(card, subject_num, code_val)
    return transform(door, code_val, card_loop)


def get_loop_size(key, subject_num, code_val):
    loop = 0
    val = 1
    while key != val:
        val = transform(subject_num, code_val, 1, val)
        loop += 1
    return loop


def transform(subject_num, code_val, loop, val=1):
    for loop_i in range(loop):
        val = (val * subject_num) % code_val
    return val


if __name__ == "__main__":
    t0 = time.time()

    test = (5764801, 17807724)
    puzzle = (1717001, 523731)
    print(day_25_part_1(*puzzle))

    print(time.time() - t0)
