from dateutil.utils import today


def new_aoc_template(day=today().day):
    with open(f"day_{day}_data.txt", "a+") as f:
        f.write("")
    with open("aoc_template", "r") as temp_f:
        lines = temp_f.readlines()
        with open(f"day_{day}.py", "a+") as new_f:
            for line in lines:
                new_f.write(rf'{line.replace("xx", str(day))}')


def load_data(fstr):
    with open(fstr, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    new_aoc_template(16)
