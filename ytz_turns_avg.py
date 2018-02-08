"""
Average number of turns needed to roll a yahtzee
"""

import time
import itertools
import argparse

from collections import Counter
from random import randrange

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", type=int, default=5, help="number of dice - d 6")
    parser.add_argument("--chunk", type=int, default=10000, help="batch size")
    return parser.parse_args()

def get_results(n):
    while True:
        tg = num = 0
        
        for i in itertools.count(1):
            dice = [randrange(6) for _ in range(n - num)]
            counts = Counter(dice)
            (moded, modec), = counts.most_common(1)

            if modec > num and moded != tg:
                tg, num = moded, modec
            else:
                num += counts[tg]

            if num == n:
                break

        yield i

def main():
    start = time.time()
    args = get_args()
    skip = 0
    try:
        for attempts, total in enumerate(itertools.accumulate(get_results(args.n)), 1):
            skip += 1
            if skip == args.chunk:
                skip = 0
                curr = time.time() - start
                print("\rAverage num of turns: {:6.3f} - {:8} attempts at {:7.3f}s, {:.2e}/s".format(
                                total / attempts,attempts, curr, attempts / curr),
                            end="", flush=True)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
