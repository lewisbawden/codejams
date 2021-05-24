from adventofcode.y2019 import aoc
import time


def day_8_part_1(data):
    proc = Processor()
    return proc.run_boot_code(data)


def day_8_part_2(data):
    proc = Processor()
    return proc.find_broken_cmd(data)


class Processor(object):
    def __init__(self):
        self.reset()
        self.instructions = self.setup_instructions()

    def reset(self):
        self.accumulator = 0
        self.next_idx = 0
        self.visited = {}
        self.exit_condition = False
        self.terminated_correctly = False

    def setup_instructions(self):
        return {
            "acc": self.instr_acc,
            "jmp": self.instr_jmp,
            "nop": self.instr_nop
        }

    def set_exit_condition(self) -> bool:
        try:
            self.exit_condition = self.visited[self.next_idx]
        except KeyError:
            self.visited[self.next_idx] = True
        return self.exit_condition

    def instr_acc(self, arg):
        if self.set_exit_condition():
            return
        self.accumulator += arg
        self.next_idx += 1

    def instr_jmp(self, arg):
        if self.set_exit_condition():
            return
        self.next_idx += arg

    def instr_nop(self, arg):
        if self.set_exit_condition():
            return
        self.next_idx += 1

    def run_boot_code(self, data):
        self.reset()
        while not self.exit_condition:
            try:
                cmd, arg = data[self.next_idx]
            except IndexError:
                self.terminated_correctly = True
                return not self.exit_condition, self.accumulator
            self.instructions[cmd](int(arg))
        self.terminated_correctly = False
        return not self.exit_condition, self.accumulator

    def find_broken_cmd(self, data):
        idx = -1
        nop_jmp = {"jmp": "nop", "nop": "jmp"}
        while not self.terminated_correctly:
            idx += 1
            try:
                data[idx][0] = nop_jmp[data[idx][0]]
                self.run_boot_code(data)
                data[idx][0] = nop_jmp[data[idx][0]]
            except KeyError:
                continue

        return idx, self.accumulator


if __name__ == "__main__":
    t0 = time.perf_counter()

    data = aoc.load_data(r"day_8_data.txt")
    parsed = [s.split() for s in data]
    print(day_8_part_2(parsed))

    print(time.perf_counter() - t0)
