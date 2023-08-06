from typing import List  # , Int  # , Dict, Tuple
import sympy as smp

# Global Solvit Symbols
A, B, C, D, E, F, G, H, J = smp.symbols("A,B,C,D,E,F,G,H,J")

GVM = {
    "A": A,
    "B": B,
    "C": C,
    "D": D,
    "E": E,
    "F": F,
    "G": G,
    "H": H,
    "J": J,
}

# smp.solve((f1,f2,f3,f4,f5,f6,f7,f8),(A,B,C,D,E,F,G,H,J))
# smp.solve([e.fx for e in self.expressions],list(GVM.values()))


class Expression:
    def __init__(self, variables: List, total: int):
        self.variables = [v.upper() for v in variables]
        self.total = total

    @property
    def fx(self):
        return smp.Eq(sum([GVM[k] for k in self.variables]), self.total)

    def __repr__(self):
        return "+".join(self.variables) + "=" + str(self.total)


def reduce_expr(x1: Expression, x2: Expression):
    i = set(tuple(x1.variables)).difference(set(tuple(x2.variables)))
    j = set(tuple(x2.variables)).difference(set(tuple(x1.variables)))
    x, y = list(i), list(j)
    d = x1.total - x2.total
    print("+".join(x), " = ", "+".join(y), " ", d)


class Puzzle:
    MainExpr = smp.Eq(sum(GVM.values()), 45)
    Symbols = list(GVM.values())

    def __init__(self, expressions: List[Expression]):
        self.expressions = expressions
        self.solution = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "E": 0,
            "F": 0,
            "G": 0,
            "H": 0,
            "J": 0,
        }

    def __repr__(self):
        return str(
            "\n".join(
                ["+".join(e.variables) + "=" + str(e.total)
                 for e in self.expressions]
            )
        )

    def var_intersects(self, *args):
        if args:
            v = self.var_expressions(args[0])
            for a in args:
                v = v.intersection(self.var_expressions(a))
            return v

    def var_expressions(self, var):
        var = var.upper()
        assert var in self.solution.keys()
        exps = set([e for e in self.expressions if var in e.variables])
        return exps

    def reduce_exprs(self):
        rform = smp.solve([e.fx for e in self.expressions] + [Puzzle.MainExpr])
        # print("We have now {0} sub solutions".format(len(rform.keys())))
        return rform

    def solution_var(self):
        rform = self.reduce_exprs()
        ks = list(rform.keys())
        xs = [k for k in Puzzle.Symbols if k not in ks][0]
        feasible_sols = [i for i in range(1, 10)]
        [
            feasible_sols.remove(x)
            for x in rform.values()
            if not isinstance(x, smp.add.Add)
        ]
        soln = self.recurse_reduce(rform, xs, feasible_sols)
        return soln

    def recurse_reduce(self, exprs, xs, feasible_sols):
        # print(feasible_sols)
        rform = exprs
        for S, F in rform.items():
            for pvr in feasible_sols:
                if isinstance(F, smp.numbers.Integer):
                    continue
                if F.subs(xs, pvr) < 1 or F.subs(xs, pvr) > 9:
                    print(S, " = ", F.subs(xs, pvr),
                          f" when {str(xs)} = ", pvr)
                    feasible_sols.remove(pvr)
                else:
                    continue
                print(feasible_sols)
        if len(feasible_sols) == 1:
            print(xs, feasible_sols)
            return xs, feasible_sols[0]
        else:
            return self.recurse_reduce(rform, xs, feasible_sols)

    def solve(self):
        sols = self.reduce_exprs()
        vsub = self.solution_var()
        for S, F in sols.items():
            self.solution[str(S)] = F.subs(*vsub)
        self.solution[str(vsub[0])] = vsub[1]
        print(self.solution)
        ...
