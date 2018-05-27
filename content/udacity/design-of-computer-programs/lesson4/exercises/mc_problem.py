def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    initial_path = [start]
    if finished(start, goal):
        return initial_path

    explored = set()
    frontier = [initial_path]
    while True:
        path = frontier.pop(0)
        state = path[-1]
        if finished(state, goal):
            return path

        for state, action in csuccessors(state).viewitems():
            if state not in explored:
                explored.add(state)
                next_path = path + [action, state]
                frontier.append(next_path)


def finished(state, goal):
    M1, C1, B1, M2, C2, B2 = state
    if goal is None:
        return (M1 == 0 and C1 == 0) or (B1 == 0 and M2 == 0 and C2 == 0)
    else:
        return state == goal


def csuccessors(state):
    M1, C1, B1, M2, C2, B2 = state

    succs = {}
    if 0 < M1 < C1 or 0 < M2 < C2:
        return succs
    for m, c in [(0, 1), (0, 2), (1, 1), (1, 0), (2, 0)]:
        if B1 > 0 and m <= M1 and c <= C1:
            nstate = (M1-m, C1-c, B1-1, M2+m, C2+c, B2+1)
            succs[nstate] = '%s%s->' % ('M'*m, 'C'*c)
        if B2 > 0 and m <= M2 and c <= C2:
            nstate = (M1+m, C1+c, B1+1, M2-m, C2-c, B2-1)
            succs[nstate] = '<-%s%s' % ('M'*m, 'C'*c)
    return succs


def test():
    assert mc_problem((0, 0, 1, 0, 0, 0)) == [(0, 0, 1, 0, 0, 0)]
    assert mc_problem((1, 1, 0, 0, 0, 1)) == [(1, 1, 0, 0, 0, 1)]
    assert mc_problem((3, 3, 1, 0, 0, 0)) == [(3, 3, 1, 0, 0, 0), 'CC->',
                                              (3, 1, 0, 0, 2, 1), '<-C',
                                              (3, 2, 1, 0, 1, 0), 'CC->',
                                              (3, 0, 0, 0, 3, 1),'<-C',
                                              (3, 1, 1, 0, 2, 0), 'MM->',
                                              (1, 1, 0, 2, 2, 1), '<-MC',
                                              (2, 2, 1, 1, 1, 0), 'MM->',
                                              (0, 2, 0, 3, 1, 1), '<-C',
                                              (0, 3, 1, 3, 0, 0), 'CC->',
                                              (0, 1, 0, 3, 2, 1), '<-M',
                                              (1, 1, 1, 2, 2, 0), 'MC->',
                                              (0, 0, 0, 3, 3, 1)]

test()
print 'pass'
