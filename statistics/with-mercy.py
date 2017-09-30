from collections import namedtuple
import math

Box = namedtuple('Box', ['count', 'cost'])

MAX_COUNT = 50
PROBABILITY = 1.0 / 60
TABLE = [
    Box(2, 2400),
    Box(5, 6000),
    Box(11, 12000),
    Box(24, 24000),
    Box(50, 48000)
]
PRIOR = [math.pow(1.0 - PROBABILITY, count) for count,__ in TABLE]


pick = [0, 0, 0, 0, 0]
solutions = []

def solve(idx, cost, count, prior):
    if count >= MAX_COUNT:
        solutions.append((cost, convert_pick(pick)))
        return

    if idx >= len(TABLE):
        return

    pick[idx] += 1
    box =TABLE[idx]
    solve(idx, cost + (prior*box.cost), count + box.count, prior*PRIOR[idx])
    pick[idx] -= 1
    solve(idx+1, cost, count, prior)


def convert_pick(pick):
    ret = []
    for i, n in enumerate(pick):
        ret.extend([TABLE[i].count for _ in range(n)])
    return ret


solve(0, 0, 0, 1.0)

answers = sorted(solutions, key=lambda t: t[0])
for cost, pick in answers[:5]:
    print "%.2f, %s" % (cost, pick)
