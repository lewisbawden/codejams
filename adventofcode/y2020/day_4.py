import time
import json
import re

ECL = "amb blu brn gry grn hzl oth".split()
HCL = r'#[0-9a-f]{6}'


def day_4_part_1(data):
    return sum(1 for entry in data if has_required_fields(entry))


def day_4_part_2(data):
    return sum(1 for entry in data if has_valid_data(entry))


def has_required_fields(entry):
    return len(entry.keys()) == 8 or (len(entry.keys()) == 7 and "cid" not in entry.keys())


def has_valid_data(e):
    try:
        valid = 1920 <= int(e["byr"]) <= 2002
        valid &= 2010 <= int(e["iyr"]) <= 2020
        valid &= 2020 <= int(e["eyr"]) <= 2030
        valid &= len(e["pid"]) == 9 and e["pid"].isnumeric()
        valid &= re.search(HCL, e["hcl"]) is not None
        valid &= (e["hgt"][-2:] == "cm" and 150 <= int(e["hgt"][:-2]) <= 193)\
                 or (e["hgt"][-2:] == "in" and 59 <= int(e["hgt"][:-2]) <= 76)
        valid &= e["ecl"] in ECL
    except KeyError:
        return False

    return valid


def parse_data(data):
    parsed_str = '{"' + ''.join(data).replace('\n\n', '"};{"').replace('\n', ' ') + '"}'
    parsed_str = parsed_str.replace(' ', '","').replace(':', '":"').split(";")
    return [json.loads(s) for s in parsed_str]


def load_data(fstr):
    with open(fstr, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    t0 = time.time()

    data = load_data(r"day_4_data.txt")
    processed = parse_data(data)

    print(day_4_part_2(processed))

    print(time.time() - t0)
