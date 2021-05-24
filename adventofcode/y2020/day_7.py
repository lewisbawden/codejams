from adventofcode.y2019 import aoc
import time


def day_7_part_1(data):
    bag_checker = get_bag_checker(data)

    bag_checker["shiny"]["gold"] = True

    total = -1  # need to subtract the shiny gold bag itself because this only counts what is True
    for line in data:
        test_bag = line.split()[0:2]
        valid = can_contain_shiny_gold_bag(bag_checker, test_bag[0], test_bag[1])

        bag_checker[test_bag[0]][test_bag[1]] = valid

        if valid:
            total += 1

    return total


def day_7_part_2(data):
    bag_checker = get_bag_checker(data)

    return get_total_bags(bag_checker, bag_checker["shiny"]["gold"])


def get_total_bags(bag_checker, bags, total=0):
    # can the bag hold any bags
    if len(bags) == 0:
        return 0

    # if the bag can hold bags, get the number of bags each bag can hold
    for num_bags, bag_style, bag_colour in bags:
        total += int(num_bags) + int(num_bags) * get_total_bags(bag_checker, bag_checker[bag_style][bag_colour])

    return total


def can_contain_shiny_gold_bag(bag_checker, bag_style, bag_colour):
    # check is bag can or cannot contain shiny gold bag
    if type(bag_checker[bag_style][bag_colour]) is bool:
        return bag_checker[bag_style][bag_colour]

    # otherwise check if contained bags can contain shiny gold bag
    valid = False
    for bag in bag_checker[bag_style][bag_colour]:
        valid |= can_contain_shiny_gold_bag(bag_checker, bag_style=bag[1], bag_colour=bag[2])
        if valid:
            break

    return valid


def get_bag_checker(data):
    rules = [line.split() for line in data]
    bags = {}
    for i, rule in enumerate(rules):
        if rule[0] not in bags.keys():
            bags[rule[0]] = {}

        bags[rule[0]][rule[1]] = [(rule[4 + j * 4: 7 + j * 4]) for j in range(int((len(rule) - 4) / 4))]

    return bags


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_7_data.txt")
    print(day_7_part_2(data))

    print(time.time() - t0)
