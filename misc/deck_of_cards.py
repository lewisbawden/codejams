import numpy as np
import time

class Suit(object):
    _colours = {"hearts": "red", "diamonds": "red", "clubs": "black", "spades": "black"}
    _values = {"hearts": 1 + 1j, "diamonds": 1 - 1j, "clubs": -1 - 1j, "spades": -1 + 1j}

    def __init__(self, suit):
        self.name = suit
        self.colour = self._colours[suit]
        self.value = self._values[suit]

    @staticmethod
    def get_suits():
        return [s for s in Suit._colours.keys()]


class CardValue(object):
    _value_names = {v: {1: 'ace', 11: 'jack', 12: 'queen', 13: 'king'}.get(v, v)
                    for v in range(1, 14)}

    def __init__(self, value):
        self.value = value
        self.name = self._value_names[value]

    @staticmethod
    def get_values():
        return [v for v in CardValue._value_names.keys()]


class Card(object):
    def __init__(self, value, suit):
        super(Card, self).__init__()
        self.value = CardValue(value)
        self.suit = Suit(suit)
        self.name = "{} of {}".format(self.value.name, self.suit.name)


class Deck(object):
    def __init__(self, cards=None):
        super(Deck, self).__init__()
        if cards is None:
            self.cards = self.create_deck()
        else:
            self.cards = cards
        self.shuffles = [getattr(self, s) for s in dir(self) if "_shuffle_" in s]

    @staticmethod
    def create_deck():
        cards = []
        for s in Suit.get_suits():
            for v in CardValue.get_values():
                cards.append(Card(v, s))
        return cards

    def deal(self):
        return self.cards.pop()

    def split(self, num_stacks=2, ratio=None):
        if ratio is None:
            ratio = [1] * num_stacks

        num_cards = len(self.cards)
        sum_ratio = sum(ratio)
        stacks = []
        sp1 = 0
        for s in range(num_stacks):
            sp0 = sp1
            sp1 += round((ratio[s] / sum_ratio) * num_cards)
            if s == num_stacks - 1:
                sp1 = num_cards
            stacks.append(Deck(self.cards[sp0: sp1]))
        return stacks

    def entropy(self):
        entropy = 0
        for i, j in zip(self.cards[:-1], self.cards[1:]):
            entropy += abs(j.value.value - i.value.value) % 12
            entropy += self._calc_suit_entropy(i.suit.value, j.suit.value)
        return entropy

    @staticmethod
    def _calc_suit_entropy(a: complex, b: complex):
        c = a*b.conjugate() - a*a.conjugate()
        return abs(c*c.conjugate()).real/4

    def shuffle(self, mode=0):
        return self.shuffles[mode]()

    def _shuffle_0(self):
        np.random.shuffle(self.cards)
        return self

    def _shuffle_1(self):
        new_deck = []
        total = len(self.cards)
        idxs = np.random.randint(0, total, total).tolist()
        while len(self.cards) > 0:
            idx = idxs.pop() % len(self.cards)
            new_deck.append(self.cards.pop(idx))
        self.cards.extend(new_deck)
        return self

    def _shuffle_2(self):
        decks = self.split(2)
        self.cards = []
        for d in decks:
            d._shuffle_1()
            self.cards.extend(d.cards)
        return self

    def _shuffle_3(self):
        new_deck = []
        total = len(self.cards)
        idxs = np.random.randint(0, total, total // 2).tolist()
        while len(self.cards) > total / 2:
            idx = idxs.pop() % len(self.cards)
            new_deck.append(self.cards.pop(idx))
        self.cards.extend(new_deck)
        return self

    def _shuffle_4(self):
        iterations = 10
        end_pos = np.random.randint(1, 10, iterations)
        num_cards = np.random.randint(10, 20, iterations)
        for it in range(iterations):
            self.cards = self.cards[num_cards[it]: -end_pos[it]] + self.cards[:num_cards[it]] + self.cards[-end_pos[it]:]
        return self


def evaluate_shuffle(mode=0):
    d = Deck()
    shuffles = np.array([])
    t0 = time.time()
    for i in range(10000):
        d.shuffle(mode)
        shuffles = np.append(shuffles, d.entropy())
    tf = time.time() - t0
    return {'mode': mode, 'duration': tf, 'mean': shuffles.mean(), 'stdev': shuffles.std(),
            'min': shuffles.min(), 'max': shuffles.max(), 'range': shuffles.max() - shuffles.min()}


if __name__ == "__main__":
    for s in range(len(Deck().shuffles)):
        print(evaluate_shuffle(s))
    exit(0)