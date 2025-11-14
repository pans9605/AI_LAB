# FIRST ORDER LOGIC → CNF CONVERTER
# ---------------------------------------------

import itertools

# Utility for generating new variable names
def new_var():
    for c in itertools.count(1):
        yield f"v{c}"

var_gen = new_var()

# ---------------------------------------------
# PARSER REPRESENTATION:
# Expr types: AND, OR, NOT, IMP, IFF, FORALL, EXISTS, PREDICATE
# ---------------------------------------------

class Expr:
    def __init__(self, op, *args):
        self.op = op
        self.args = list(args)

    def __repr__(self):
        if self.op == "PRED":
            return self.args[0]
        elif self.op in ["FORALL", "EXISTS"]:
            return f"({self.op} {self.args[0]}. {self.args[1]})"
        elif self.op == "NOT":
            return f"(¬{self.args[0]})"
        else:
            return f"({self.args[0]} {self.op} {self.args[1]})"


# Convenient shortcuts
def AND(a, b): return Expr("AND", a, b)
def OR(a, b): return Expr("OR", a, b)
def NOT(a): return Expr("NOT", a)
def IMP(a, b): return Expr("IMP", a, b)
def IFF(a, b): return Expr("IFF", a, b)
def FORALL(v, e): return Expr("FORALL", v, e)
def EXISTS(v, e): return Expr("EXISTS", v, e)
def P(t): return Expr("PRED", t)

# ---------------------------------------------
# STEP 1: Eliminate → and ↔
# ---------------------------------------------
def remove_implications(expr):
    if expr.op == "IMP":
        # A → B == ¬A ∨ B
        return OR(NOT(remove_implications(expr.args[0])),
                  remove_implications(expr.args[1]))
    if expr.op == "IFF":
        # A ↔ B == (A→B) ∧ (B→A)
        A = remove_implications(expr.args[0])
        B = remove_implications(expr.args[1])
        return AND(OR(NOT(A), B), OR(NOT(B), A))
    if expr.op in ["AND", "OR"]:
        return Expr(expr.op, *(remove_implications(a) for a in expr.args))
    if expr.op == "NOT":
        return NOT(remove_implications(expr.args[0]))
    if expr.op in ["FORALL", "EXISTS"]:
        return Expr(expr.op, expr.args[0], remove_implications(expr.args[1]))
    return expr

# ---------------------------------------------
# STEP 2: Move negations inward (NNF)
# ---------------------------------------------
def move_negation_inward(expr):
    if expr.op == "NOT":
        x = expr.args[0]

        if x.op == "NOT":  
            return move_negation_inward(x.args[0])

        if x.op == "AND":  
            return OR(move_negation_inward(NOT(x.args[0])),
                      move_negation_inward(NOT(x.args[1])))

        if x.op == "OR":
            return AND(move_negation_inward(NOT(x.args[0])),
                       move_negation_inward(NOT(x.args[1])))

        if x.op == "FORALL":
            return EXISTS(x.args[0], move_negation_inward(NOT(x.args[1])))

        if x.op == "EXISTS":
            return FORALL(x.args[0], move_negation_inward(NOT(x.args[1])))

        return expr

    if expr.op in ["AND", "OR"]:
        return Expr(expr.op,
                    move_negation_inward(expr.args[0]),
                    move_negation_inward(expr.args[1]))

    if expr.op in ["FORALL", "EXISTS"]:
        return Expr(expr.op, expr.args[0], move_negation_inward(expr.args[1]))

    return expr

# ---------------------------------------------
# STEP 3: Standardize variables
# ---------------------------------------------
def standardize(expr, mapping=None):
    if mapping is None:
        mapping = {}

    if expr.op == "PRED":
        return expr

    if expr.op in ["AND", "OR"]:
        return Expr(expr.op,
                    standardize(expr.args[0], mapping),
                    standardize(expr.args[1], mapping))

    if expr.op == "NOT":
        return NOT(standardize(expr.args[0], mapping))

    if expr.op in ["FORALL", "EXISTS"]:
        v = expr.args[0]
        new_v = next(var_gen)
        mapping[v] = new_v
        return Expr(expr.op, new_v, standardize(expr.args[1], mapping))

    return expr

# ---------------------------------------------
# STEP 4: Skolemization
# ---------------------------------------------
def skolemize(expr, bound_vars=None):
    if bound_vars is None:
        bound_vars = set()

    if expr.op == "FORALL":
        bound_vars.add(expr.args[0])
        return FORALL(expr.args[0], skolemize(expr.args[1], bound_vars))

    if expr.op == "EXISTS":
        var = expr.args[0]
        skolem_const = f"F_{var}"
        return skolemize(expr.args[1].__repr__().replace(var, skolem_const))

    if expr.op in ["AND", "OR"]:
        return Expr(expr.op,
                    skolemize(expr.args[0], bound_vars),
                    skolemize(expr.args[1], bound_vars))

    if expr.op == "NOT":
        return NOT(skolemize(expr.args[0], bound_vars))

    return expr

# ---------------------------------------------
# STEP 5: Drop universal quantifiers
# ---------------------------------------------
def drop_universal(expr):
    if expr.op == "FORALL":
        return drop_universal(expr.args[1])
    if expr.op in ["AND", "OR"]:
        return Expr(expr.op,
                    drop_universal(expr.args[0]),
                    drop_universal(expr.args[1]))
    if expr.op == "NOT":
        return NOT(drop_universal(expr.args[0]))
    return expr

# ---------------------------------------------
# STEP 6: Distribute OR over AND → CNF
# ---------------------------------------------
def distribute(expr):
    if expr.op == "OR":
        A = distribute(expr.args[0])
        B = distribute(expr.args[1])

        if A.op == "AND":
            return AND(distribute(OR(A.args[0], B)),
                       distribute(OR(A.args[1], B)))

        if B.op == "AND":
            return AND(distribute(OR(A, B.args[0])),
                       distribute(OR(A, B.args[1])))

        return OR(A, B)

    if expr.op == "AND":
        return AND(distribute(expr.args[0]), distribute(expr.args[1]))

    return expr

# ---------------------------------------------
# MASTER FUNCTION
# ---------------------------------------------
def to_cnf(expr):
    expr = remove_implications(expr)
    expr = move_negation_inward(expr)
    expr = standardize(expr)
    expr = skolemize(expr)
    expr = drop_universal(expr)
    expr = distribute(expr)
    return expr


# ---------------------------------------------
# EXAMPLE USE
# ---------------------------------------------

formula = IMP(P("Rich(x)"), AND(P("Heart(x)"), P("Person(x)")))
cnf_result = to_cnf(formula)

print("\nCNF RESULT =")
print(cnf_result)

