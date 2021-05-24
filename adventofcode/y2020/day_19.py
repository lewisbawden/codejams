from adventofcode.y2019 import aoc
import time
import re


def day_19_part_1(rules, messages):
    pattern = get_re_pattern(rules, "0")
    reg_pat = re.compile(pattern)
    return len([message for message in messages if reg_pat.match(message) is not None])


def get_re_pattern(rules, main_key):

    def expand_rule(key=main_key):
        next_keys, rule = rules[key]

        if rule in ["a", "b"]:
            return rule

        while len(next_keys) > 0:
            next_key = next_keys.pop()
            expanded = " {} ".format(expand_rule(next_key))
            rule = re.sub("{} | {}|^{}$".format(*[next_key] * 3), expanded, rule)
        rules[key] = [list(), rule]
        return rules[key][1]

    pattern = expand_rule(main_key).replace(" ", "")
    return "^{}$".format(pattern)


def day_19_part_2(rules, messages):
    count = 1
    ls, rs = "42 ", " 31"
    rules = update_rules(rules, ls, rs, count)

    all_matches = []
    match_totals = [1] * 3
    while sum(match_totals[-3:]) != 0:
        count += 1
        pattern = get_re_pattern(rules, "0")
        reg_pat = re.compile(pattern)
        matches = [message for message in messages if reg_pat.match(message) is not None]
        messages = [message for message in messages if message not in all_matches]
        all_matches += matches
        match_totals.append(len(matches))
        rules = update_rules(rules, ls, rs, count)
    return len(all_matches)


def update_rules(rules, ls, rs, count):
    rules["0"] = [['8', '11'], '8 11']
    rules["8"] = [['8', '42'], '( 42 )+']
    rules["11"] = [['11', '31', '42'], ls * count + rs * count]
    return rules


def parse_input(data):
    messages = [line.replace("\n", "") for line in data if ":" not in line]
    rules = {line.split(":")[0]: line.replace("\n", "").split(": ")[1].replace('"', '') for line in data if ":" in line}

    for key, rule in rules.items():
        # ensure keys are sorted in ascending order so popped key is highest, and will not be a substring of another key
        child_keys = sorted(set(r for r in rule.replace("|", "").split() if r.isnumeric()), key=lambda x: int(x))
        rules[key] = [child_keys, rule]
        if "|" in rule:
            rules[key][1] = rule.replace(rule, "(( {} ))".format("  ".join(rule.split()))).replace("|", " )|( ")
        elif rule not in ["a", "b"]:
            rules[key][1] = rule.replace(rule, "  ".join(rule.split()))

    return rules, messages


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_19_data.txt")
    print(day_19_part_2(*parse_input(data)))

    print(time.time() - t0)
