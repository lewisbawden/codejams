from adventofcode.y2019 import aoc
import time


class Bus:
    def __init__(self, id, order, posn):
        self.id = id
        self.order = order
        self.tc = id
        self.posn = posn
        self.step = id


def day_13_part_1(data):
    t0 = int(data[0][0:-1])
    buses = [int(b) for b in data[1].split(",") if b.isnumeric()]
    tf = t0
    while True:
        for bus in buses:
            if tf % bus == 0:
                return bus, t0, tf, bus * (tf - t0)
        tf += 1


def day_13_part_2(data):
    buses = parse_data(data)
    id_sorted_buses = sorted(buses, key=lambda bus: bus.id, reverse=True)
    highest_bus = id_sorted_buses[0]
    for bus in id_sorted_buses:
        bus.tc_offset = bus.posn - highest_bus.posn

    tc = 0
    while True:
        try:
            tc += highest_bus.step
            check_timecodes(tc, id_sorted_buses)
        except StopIteration:
            return tc + buses[0].tc_offset


def check_timecodes(tc, buses):
    try:
        for bus in buses[1:]:
            # check if the bus id is factor of the appropriately offset timecode
            if (tc + bus.tc_offset) % bus.id != 0:
                raise BusTimecodeError
            # can step up in multiples of their LCM from now on since any lower step will not satisfy this condition
            if buses[0].step % bus.id != 0:
                # make sure this new bus id is included in buses[0].step if not already
                buses[0].step *= bus.id
        raise StopIteration
    except BusTimecodeError:
        pass


class BusTimecodeError(Exception):
    """ Invalid bus timecode"""


def parse_data(data):
    parsed = []
    max_id = 0
    bus_order_idx = 0
    for n, s in enumerate(data[1].split(",")):
        if s.isnumeric():
            parsed.append(Bus(int(s), bus_order_idx, n))
            max_id = max(int(s), max_id)
            bus_order_idx += 1
    return parsed


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_13_data.txt")

    tests = [
        [3417, "17,x,13,19"],
        [754018, "67,7,59,61"],
        [779210, "67,x,7,59,61"],
        [1261476, "67,7,x,59,61"],
        [1068781, "7,13,x,x,59,x,31,19"],
        [1202161486, "1789,37,47,1889"]
    ]

    for test in tests:
        ans = day_13_part_2(test)
        print(test[0] == ans, test[0], ":", ans)

    print(day_13_part_2(data))

    print(time.time() - t0)
