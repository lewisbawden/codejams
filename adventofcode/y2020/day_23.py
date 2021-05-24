import time


def day_23_part_1(cup_labels, moves, total_cups=None):
    cc = CrabCupsClockGame(cup_labels)
    return cc.make_moves(moves, False)


class Cup:
    def __init__(self, label, left=None, right=None):
        self.label = label
        self.left = label - 1 if left is None else left
        self.right = label + 1 if right is None else right

    def set_left(self, ar, i):
        try:
            self.left = int(ar[i])
        except IndexError:
            self.left = None

    def set_right(self, ar, i):
        try:
            self.right = int(ar[i])
        except IndexError:
            self.right = None


class CrabCupsClockGame:
    def __init__(self, cup_labels: str, total_cups=None):
        self.result = ""
        self.current_key = int(cup_labels[0])
        self.current_cup = Cup(int(cup_labels[0]))
        self.dest_cup = None
        self.picked_cups = []
        self.total_cups = total_cups if total_cups is not None else len(cup_labels)
        self.cups = {int(d): Cup(int(d)) for d in cup_labels}
        # stich inner cups
        for i, d in enumerate(cup_labels):
            self.cups[int(d)].set_left(cup_labels, i - 1)
            self.cups[int(d)].set_right(cup_labels, i + 1)
        # stitch end cups
        self.cups[int(cup_labels[0])].left = self.total_cups
        self.cups[int(cup_labels[-1])].right = int(cup_labels[0]) if total_cups is None else len(cup_labels) + 1
        if total_cups is not None:
            self.cups.update({d: Cup(d, d - 1, d + 1) for d in range(len(cup_labels) + 1, self.total_cups + 1)})
            # stitch ends of extra cups for v2
            self.cups[len(cup_labels) + 1].left = int(cup_labels[-1])
            self.cups[self.total_cups].right = int(cup_labels[0])

    def _pick_cups(self):
        self.picked_cups = []
        self.current_cup = self.cups[self.current_key]
        self.current_key = self.current_cup.right
        for i in range(3):
            self.picked_cups.append(self.cups[self.current_key])
            self.current_key = self.picked_cups[i].right
        self.current_cup.right = self.current_key
        self.cups[self.current_key].left = self.current_cup.label

    def _get_destination_cup(self):
        label = self.current_cup.label
        while True:
            label -= 1
            if label == 0:
                label = self.total_cups
            if label not in [pc.label for pc in self.picked_cups]:
                self.dest_cup = self.cups[label]
                return

    def _place_cups(self):
        original_label = self.dest_cup.right
        self.dest_cup.right = self.picked_cups[0].label
        self.cups[self.picked_cups[0].label].left = self.dest_cup.label
        self.cups[original_label].left = self.picked_cups[-1].label
        self.cups[self.picked_cups[-1].label].right = original_label

    def _print_cups(self, m):
        print(m, "current: ", self.current_cup.label)
        print(m, "pick up: ", [pc.label for pc in self.picked_cups])
        print(m, "destination: ", self.dest_cup.label)
        print(m, "next cup: ", self.current_key)
        print()

    def _make_move(self, m, debug):
        self._pick_cups()
        self._get_destination_cup()
        self._place_cups()
        if debug:
            self._print_cups(m)

    def make_moves(self, moves, v2, debug=False):
        percent = 0
        print_factor = 1000000
        start = time.time()
        for m in range(1, moves + 1):
            self._make_move(m, debug=debug)
            if m % print_factor == 0:
                percent += (100 * (print_factor / moves))
                print(percent, "%", time.time() - start)
        return self._get_result(v2)

    def _get_result(self, v2):
        if v2:
            self.result = [self.cups[1].right, self.cups[self.cups[1].right].right]
        else:
            cup = self.cups[1]
            while cup.right != 1:
                cup = self.cups[cup.right]
                self.result += str(cup.label)
        return self.result


def day_23_part_2(cup_labels, moves, total_cups):
    cc = CrabCupsClockGame(cup_labels, total_cups)
    return cc.make_moves(moves, True)


if __name__ == "__main__":
    t0 = time.time()

    test = "389125467"
    puzzle = "467528193"
    print(day_23_part_1(puzzle, moves=100))
    print(day_23_part_2(puzzle, moves=10000000, total_cups=1000000))

    print(time.time() - t0)
