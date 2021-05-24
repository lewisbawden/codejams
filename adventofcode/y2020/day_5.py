import time
FBLR_map = [("F", "0"), ("B", "1"), ("L", "0"), ("R", "1"), ("\n", "")]


def day_5_part_1(data):
    return data[-1][0]*8 + data[-1][1]


def day_5_part_2(data):
    seat_ids = [seat[0]*8 + seat[1] for seat in data]
    missing = [seat_ids[i] != seat_ids[i-1] + 1 for i in range(1, len(seat_ids))]
    return [seat_ids[i + 1] - 1 for i, m in enumerate(missing) if m][0]


def convert_boarding_passes_to_seats(data):
    def convert_boarding_pass_to_binary(line):
        for i, o in FBLR_map:
            line = line.replace(i, o)
        return [int(li) for li in line]

    def convert_binary_to_seat(b):
        row = sum(b[i]*2**(6-i) for i in range(7))
        col = sum(b[i+7]*2**(2-i) for i in range(3))
        return row, col

    binary_seats = [convert_boarding_pass_to_binary(l) for l in data]
    return [convert_binary_to_seat(b) for b in binary_seats]


def load_data(fstr):
    with open(fstr, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    t0 = time.time()

    data = load_data(r"day_5_data.txt")
    seats = convert_boarding_passes_to_seats(data)

    print(day_5_part_2(sorted(seats)))

    print(time.time() - t0)
