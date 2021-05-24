from adventofcode.y2019 import aoc
import time
import day_16


def day_21_part_1(foods, allergens):
    foods, allergens = find_allergen_possibilities(foods, allergens)
    allergens = day_16.determine_fields({k: [v for v in allergens[k]] for k in allergens.keys()})

    ingredients = []
    allergens_translated = [v[0] for v in allergens.values()]
    for food_idx, food in foods.items():
        ingredients += [i for i in food["ingredients"] if i not in allergens_translated]

    print("day_21_part_2:", ",".join([allergens[k][0] for k in sorted(allergens.keys())]))
    return len(ingredients)


def find_allergen_possibilities(foods, allergens):
    for allergen in allergens.keys():
        for food_key, food in foods.items():
            if allergen in food['allergens']:
                if allergens[allergen] is None:
                    allergens[allergen] = food["ingredients"]
                else:
                    allergens[allergen] = allergens[allergen].intersection(food["ingredients"])
    return foods, allergens


def parse_data(data):
    all_allergens = []
    foods = {}
    for i, food in enumerate(data):
        ingredients_i, allergens_i = food.split("(")
        foods[i] = {}
        foods[i]["ingredients"] = set(ingredients_i.split())
        cleaned_allergens = clean_allergens(allergens_i)
        foods[i]["allergens"] = cleaned_allergens
        all_allergens += cleaned_allergens

    return foods, {a: None for a in set(all_allergens)}


def clean_allergens(line):
    rem = ["contains", ",", ")", "\n"]
    for r in rem:
        line = line.replace(r, "")
    return line.split()


if __name__ == "__main__":
    t0 = time.time()

    data = aoc.load_data(r"day_21_data.txt")
    print(day_21_part_1(*parse_data(data)))

    print(time.time() - t0)
