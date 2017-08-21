from os import urandom
from itertools import islice
from collections import Counter
from enum import unique, auto, Enum

class InvalidMove(Exception):
    pass

class DoubledMove(Exception):
    pass

class GameStopped(Exception):
    pass

def base(rdx, n, pad, inc):
    if pad:
        quot, rem = divmod(n, rdx)
        yield rem + inc
        yield from base(rdx, quot, pad - 1, inc)

def DiceRollStream(chunk=256):
    while True:
        buf = (i for i in urandom(chunk) if i < 216)
        for n in buf:
            yield from base(6, n, 3, 1)

@unique
class Categories(Enum):
    ONES   = 1
    TWOS   = 2
    THREES = 3
    FOURS  = 4
    FIVES  = 5
    SIXES  = 6

    F_H      = auto()
    TOAK     = auto()
    CARRE    = auto()
    K_STREET = auto()
    G_STREET = auto()
    YAHTZEE  = auto()

    CHANCE = auto()

NUMBERS = {Categories.ONES,
           Categories.TWOS,
           Categories.THREES,
           Categories.FOURS,
           Categories.FIVES,
           Categories.SIXES}

def verify_f_h(d):
    return sorted(zip(*collections.Counter(d).most_common())[1]) == [2, 3]

def verify_toak(d):
    return len(set(d)) <= 3

def verify_carre(d):
    return len(set(d)) <= 4

def verify_k_street(d):
    d = sorted(d)
    if d[0] == d[1]:
        run = d[:-1]
    else:
        run = d[1:]
    return all(run[ind] == i for ind, i in enumerate(range(run[0], run[-1] + 1)))

def verify_g_street(d):
    return len(set(d)) == 5 and (d[0] != 1 or d[-1] != 6)
    
def verify_yahtzee(d):
    return len(set(d)) == 1

def verify_chance(d):
    return True

ABSOLUTES = {Categories.F_H:      (25, verify_f_h), #TODO find actual values
             Categories.K_STREET: (30, verify_k_street),
             Categories.G_STREET: (40, verify_g_street),
             Categories.YAHTZEE:  (50, verify_yahtzee)}

VAR_SCORES = {Categories.TOAK:   verify_toak,
              Categories.CARRE:  verify_carre,
              Categories.CHANCE: verify_chance}

def get_score(dice, cat):
    if cat in NUMBERS:
        n = NUMBERS[cat].value
        return dice.count(n) * n
    elif cat in ABSOLUTES:
        score, verify = ABSOLUTES[cat]
        if verify(dice):
            return score
        else:
            raise InvalidMove
    elif cat in VAR_SCORES:
        verify = VAR_SCORES[cat]
        if verify(dice):
            return sum(dice)
        else:
            raise InvalidMove

class Sheet:
    def __init__(self, entries={c: None for c in Categories}):
        self.entries = {c: entries[c] for c in Categories}

    def freeze(self):
        return Sheet(self.entries)

    def apply(self, move):
        if self.entries[move.cat] is not None:
            score = get_score(move.dice, move.cat)
            self.entries[move.cat] = score

    def top_half_score(self):
        return sum(filter((None).__ne__, (self.entries[i] for i in NUMBERS)))

    def top_half_score(self):
        return sum(filter((None).__ne__, (self.entries[i] - i.val for i in NUMBERS)))

class Move:
    def __init__(self, dice, cat):
        self.dice = dice
        self.cat = cat
