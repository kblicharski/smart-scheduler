from constraint import Problem, Solver, Constraint

problem = Problem()


class TimeObj():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return '[{}-{}]'.format(self.start, self.end)

problem.addVariable('a', [TimeObj(11, 13), TimeObj(9, 11), TimeObj(10, 12)])
problem.addVariable('b', [TimeObj(12, 14), TimeObj(9, 10)])


def constraint_func(a, b):
    return a.start >= b.end or a.end <= b.start

problem.addConstraint(constraint_func, ['a', 'b'])

solution_set = problem.getSolutions()

for solution in solution_set:
    for key in solution:
        print(key + ' ' + str(solution[key]))
    print('\n')
