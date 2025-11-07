# -------------------- FOL Resolution engine (supports variables) --------------------
from itertools import combinations
import re

def is_variable(t): return t[0].islower()

def parse_literal(s):
    s=s.strip()
    neg=False
    if s.startswith("~") or s.startswith("¬"):
        neg=True; s=s[1:]
    pred=s.split("(")[0]
    args=s[s.index("(")+1:s.index(")")].split(",")
    return (("~"+pred) if neg else pred, tuple([a.strip() for a in args]))

def comp(l):
    if l[0].startswith("~"): return (l[0][1:],l[1])
    return ("~"+l[0],l[1])

def unify(x,y,subs):
    if subs is None: return None
    if x==y: return subs
    if is_variable(x): return unify_var(x,y,subs)
    if is_variable(y): return unify_var(y,x,subs)
    return None

def unify_var(var,x,subs):
    if var in subs: return unify(subs[var],x,subs)
    if x in subs: return unify(var,subs[x],subs)
    new=subs.copy(); new[var]=x; return new

def apply(l,subs):
    pred,args=l; return (pred,tuple(subs.get(a,a) for a in args))

def resolve(ci,cj):
    new=set()
    for li in ci:
        for lj in cj:
            if li[0]==comp(lj)[0] and len(li[1])==len(lj[1]):
                subs=unify(li[1],lj[1],{})
                if subs is not None:
                    N=set(apply(l,subs) for l in (ci|cj) if l!=li and l!=lj)
                    new.add(frozenset(N))
    return new

def resolution_FOL(KB,query):
    KB=[set(parse_literal(l) for l in clause) for clause in KB]
    KB.append({parse_literal("~"+query)})
    KB=set(frozenset(c) for c in KB)
    while True:
        new=set()
        for ci,cj in combinations(KB,2):
            r=resolve(ci,cj)
            if frozenset() in r: return True
            new|=r
        if new.issubset(KB): return False
        KB|=new

# ------------------- USER INPUT -------------------
KB=[]
n=int(input("How many clauses? "))
print("Enter each clause as comma separated literals for example:  ~P(x),Q(x)")

for i in range(n):
    clause=input(f"Clause {i+1}: ")
    parts=[p.strip() for p in clause.split(",")]
    KB.append(set(parts))

query=input("Enter query literal (ex: Likes(John,peanuts)): ")

print("\nRESULT =", resolution_FOL(KB,query))
