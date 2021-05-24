from adventofcode.y2019 import aoc
import time
import re


def day_14_part_1(data):
    memory = {}
    mask = ""
    for cmd, val in data:
        if "mask" in cmd:
            mask = val
        if "mem" in cmd:
            bval = get_binary(val)
            mem_id = int(get_mem_loc(cmd))
            memory[mem_id] = apply_mask_v1(mask, bval)
    return sum(memory.values())


def apply_mask_v1(mask, bval):
    out = ["0"]*len(mask)
    for i in range(len(bval)):
        out[-1 - i] = bval[-1 - i]
    for i in range(len(mask)):
        m = mask[-1 - i]
        if m != "X":
            out[-1 - i] = m
    return int("".join(out), 2)


def get_binary(inp: str) -> str:
    return f"{int(inp):b}"


def get_mem_loc(inp: str) -> str:
    return re.match("mem\[(\d*)\]", inp).group(1)


def day_14_part_2(data):
    memory = {}
    mask = ""
    for cmd, val in data:
        if "mask" in cmd:
            mask = val
        if "mem" in cmd:
            mem_id = get_binary(get_mem_loc(cmd))
            memory = apply_mask_v2(mask, mem_id, memory, int(val))
    return sum(memory.values())


def apply_mask_v2(mask, orig_mem_id, memory, val):
    fbmask = get_floating_bit_mask(mask, orig_mem_id)
    mem_ids = set_x_bits(fbmask)
    for mem_id in mem_ids:
        memory["".join(mem_id)] = val
    return memory


def set_x_bits(fbmask, mem_ids=[]):
    if fbmask.count("X") == 0:
        return [fbmask]

    x_loc = "".join(fbmask).find("X")
    new_mem_ids = []
    for fb in range(2):
        mem_id = fbmask.copy()
        mem_id[x_loc] = str(fb)
        new_mem_ids += set_x_bits(mem_id, mem_ids)

    return mem_ids + new_mem_ids


def get_floating_bit_mask(mask, mem_id):
    out = ["0"] * len(mask)
    for i in range(len(mask)):
        m = mask[-1 - i]
        if m == "0":
            out[-1 - i] = get_bit(mem_id, -1 - i, "0")
        else:
            out[-1 - i] = m
    return out


def get_bit(val, idx, default):
    try:
        return val[idx]
    except IndexError:
        return default


if __name__ == "__main__":
    t0 = time.time()

    data = [d.replace("\n", "").split("=") for d in aoc.load_data(r"day_14_data.txt")]
    print(day_14_part_2(data))

    print(time.time() - t0)
