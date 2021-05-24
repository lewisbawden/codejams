from adventofcode.y2019 import aoc
import time
import re
import numpy as np


def day_16_part_1(rules, myticket: list, tickets: list):
    error_rate = []
    for ticket in tickets:
        for v in ticket:
            if not valid_field_found(rules, v):
                error_rate.append(v)
    return sum(error_rate)


def valid_rule(rule, v):
    if rule[1] <= v <= rule[2] or rule[3] <= v <= rule[4]:
        return True
    return False


def valid_field_found(rules, v):
    return any(valid_rule(rule, v) for rule in rules)


def valid_ticket(ticket, rules):
    for v in ticket:
        if not valid_field_found(rules, v):
            return False
    return True


def day_16_part_2(rules, myticket: list, tickets: list):
    valid = np.array([ticket for ticket in tickets if valid_ticket(ticket, rules)])

    # how many columns have every value matching just a single rule
    # dict of {col idx: all rule idxs where all values in col match that rule}
    possible_fields = {i: [j for j, rule in enumerate(rules) if all((valid_rule(rule, v) for v in valid[:, i]))]
                       for i in range(valid.shape[1])}

    # dict of {col idx: rule idx}
    known_fields = determine_fields(possible_fields)

    dept_fields = [myticket[k] for k, v in known_fields.items() if "departure" in rules[v[0]][0]]

    ans = 1
    for i in dept_fields:
        ans *= i
    return ans


def determine_fields(possible_fields):
    finished = False
    popped = []
    remove = -1
    while not finished:
        finished = True
        for k, v in possible_fields.items():
            if len(v) == 1 and v[0] not in popped:
                remove = v[0]
                popped.append(v[0])
                finished = False
                break
        for k, v in possible_fields.items():
            if remove in v and len(v) != 1:
                remove_idx = v.index(remove)
                v.pop(remove_idx)
    return possible_fields


def parse_ticket_doc(data):
    rules, myticket, tickets = "".join(data).split("\n\n")

    expr = re.compile("(.*)\: (\d*)-(\d*) or (\d*)-(\d*)")
    rules = [[expr.match(rule).group(i) for i in range(1, 6)] for rule in rules.split("\n")]
    rules = [[line[0]] + [int(s) for s in line if s.isnumeric()] for line in rules]

    myticket = myticket.split("\n")[1].split(",")
    myticket = [int(s) for s in myticket if s.isnumeric()]

    tickets = [ticket.split(",") for ticket in tickets.split("\n")[1:]]
    tickets = [[int(s) for s in line if s.isnumeric()] for line in tickets]

    return rules, myticket, tickets


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_16_data.txt")
    print(day_16_part_2(*parse_ticket_doc(data)))

    print(time.time() - t0)
