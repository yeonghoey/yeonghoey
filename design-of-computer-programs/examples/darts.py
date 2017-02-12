# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""


SINGLES = set(range(1, 21) + [25])
DOUBLES = set([n*2 for n in SINGLES])
TRIPLES = set([n*3 for n in SINGLES if n != 25])
SCORES = sorted(SINGLES | DOUBLES | TRIPLES, reverse=True)

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""

    def throw(scores):
        current = sum(scores)
        if current > total:
            return None
        if current == total:
            return scores if scores[-1] in DOUBLES else None
        if len(scores) < 3:
            for d in SCORES:
                ret = throw(scores + [d])
                if ret is not None:
                    return ret
    scores = throw([])
    return [dart(s, i == len(scores)-1) for i, s in enumerate(scores)] if scores is not None else None


def dart(score, is_last):
    if score in DOUBLES and is_last:
        return 'D' + notation(score // 2)
    elif score in SINGLES:
        return 'S' + notation(score // 3)
    elif score in TRIPLES:
        return 'T' + notation(score // 3)
    if score in DOUBLES:
        return 'D' + notation(score // 2)
    else:
        raise ValueError('Invalid score')


def notation(number):
    return str(number) if number != 25 else 'B'



"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""


SECTIONS = '20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5'.split()
ADJACENTS = {}
for i in range(1, len(SECTIONS)-1):
    left, x, right = SECTIONS[i-1:i+2]
    ADJACENTS[x] = [left, right]
ADJACENTS['20'] = ['5', '1']
ADJACENTS['5'] = ['12', '20']
ADJACENTS['B'] = SECTIONS


from collections import defaultdict


def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    probabilities = [(t2, p2) for t, p in  ring_miss(target, miss)
                              for t2, p2 in section_miss(t, p, miss)]
    table = defaultdict(float)
    for t, p in probabilities:
        table[t] += p
    return dict(table)


def ring_miss(target, miss):
    ring, section = target[0], target[1:]
    bull_section_miss_targets = ['S'+a for a in ADJACENTS['B']]
    miss_events = ([('D'+section, 0.25*miss)] + \
                   unidist(bull_section_miss_targets, 0.75*miss) if target == 'SB' else
                   [('S'+section, miss)] + \
                   unidist(bull_section_miss_targets, 2*miss)    if target == 'DB' else
                   [('S'+section, 0.5*miss)]                     if ring == 'D' else
                   [('S'+section, miss)]                         if ring == 'T' else
                   [('D'+section, 0.1*miss), ('T'+section, 0.1*miss)])
    pass_event = (target, 1-sum(p for _, p in miss_events))
    return [pass_event] + miss_events


def section_miss(target, p, miss):
    ring, section = target[0], target[1:]
    adjacents = ADJACENTS[section]
    pass_event = (target, p*(1-miss))
    miss_ring = ring if section != 'B' else 'S'
    miss_events = unidist([miss_ring+a for a in adjacents], p*miss)
    return [pass_event] + miss_events


def unidist(cases, total_p):
    p = total_p / len(cases)
    return [(c, p) for c in cases]


def best_target(miss):
    "Return the target that maximizes the expected score."
    targets = ['SB', 'DB'] + [r+s for r in 'SDT' for s in SECTIONS]

    def E(target):
        table = outcome(target, miss)
        return sum(score(t)*p for t, p in table.viewitems())

    return max(targets, key=E)


def score(target):
    ring, section = target[0], target[1:]
    mul = dict(S=1., D=2., T=3.)[ring]
    point = int(section) if section != 'B' else 25
    return mul * point


def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1),
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))
