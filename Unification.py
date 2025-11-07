def is_var(t):
    return len(t) == 1 and t.islower()

def parse_term(term):
    term = term.strip()
    if "(" not in term:
        return term, []
    func = term[:term.index("(")]
    args = []
    inner = term[term.index("(")+1:-1]
    balance = 0
    current = ""
    for ch in inner:
        if ch == ',' and balance == 0:
            args.append(current.strip())
            current = ""
        else:
            current += ch
            if ch == '(':
                balance += 1
            elif ch == ')':
                balance -= 1
    if current:
        args.append(current.strip())
    return func, args

def apply(subs, term):
    # apply substitutions inside nested structures
    if is_var(term) and term in subs:
        return apply(subs, subs[term])
    func, args = parse_term(term)
    if not args:
        return subs.get(term, term)
    new_args = [apply(subs, a) for a in args]
    return f"{func}({','.join(new_args)})"

def occurs_check(var, term, subs):
    term = apply(subs, term)
    if var == term:
        return True
    if "(" in term:
        f, args = parse_term(term)
        return any(occurs_check(var, a, subs) for a in args)
    return False

def unify(expr1, expr2):
    subs = {}
    stack = [(expr1, expr2)]

    while stack:
        t1, t2 = stack.pop()

        t1 = apply(subs, t1)
        t2 = apply(subs, t2)

        if t1 == t2:
            continue

        # variable cases
        if is_var(t1):
            if occurs_check(t1, t2, subs):
                return None
            subs[t1] = t2
            continue

        if is_var(t2):
            if occurs_check(t2, t1, subs):
                return None
            subs[t2] = t1
            continue

        # non-variable: must match functor and unify arguments
        f1, args1 = parse_term(t1)
        f2, args2 = parse_term(t2)

        if f1 != f2 or len(args1) != len(args2):
            return None

        for a1, a2 in zip(args1, args2):
            stack.append((a1, a2))

    # final substitution map
    return {v: apply(subs, t) for v, t in subs.items()}

# ------ TEST ------
tests = [
    ("Older(father(y), y)", "Older(father(x), john)"), # should unify
    ("P(A,B,B)", "P(x,y,z)"),  
    ("Q(y,G(A,B))", "Q(G(x,x),y)"),   # FAIL test
    ("Older(father(y),y)", "Older(father(x), john)"),           # arity mismatch FAIL
    ("knows(john, x)", "knows(x, jack)"), # FAIL test
    ("knows(x, y, z)", "knows(john, jack, tom)"),
    ("knows(father(y), y)", "knows(x, x)"),
]

for a, b in tests:
    r = unify(a, b)
    print(f"{a}  vs  {b}  => ", "FAILED" if r is None else r)
