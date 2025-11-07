# Forward Chaining for FOL with user input
# You can enter statements like in the screenshot (FOL format)

def infer(facts, rules):
    inferred = set(facts)
    while True:
        added = False
        for rule in rules:
            left, right = rule.split("=>")
            left_parts = [p.strip() for p in left.split("^")]
            right = right.strip()

            bindings = {}
            match = True
            for part in left_parts:
                pred, args = part.split("(")
                args = args[:-1].split(",")
                found = False
                for fact in inferred:
                    if fact.startswith(pred):
                        fact_args = fact[fact.find("(")+1:-1].split(",")
                        if len(fact_args) == len(args):
                            temp_bind = bindings.copy()
                            consistent = True
                            for a, f in zip(args, fact_args):
                                if a.islower():  # variable
                                    if a in temp_bind and temp_bind[a] != f:
                                        consistent = False
                                        break
                                    temp_bind[a] = f
                                elif a != f:
                                    consistent = False
                                    break
                            if consistent:
                                bindings = temp_bind
                                found = True
                                break
                if not found:
                    match = False
                    break

            if match:
                pred, args = right.split("(")
                args = args[:-1].split(",")
                result = pred + "(" + ",".join([bindings.get(a, a) for a in args]) + ")"
                if result not in inferred:
                    print(f"Inferred: {result}")
                    inferred.add(result)
                    added = True
        if not added:
            break
    return inferred


# ---------- MAIN ----------
print("=== Forward Chaining in First Order Logic ===\n")

# Input facts
n = int(input("Enter number of facts: "))
facts = [input(f"Fact {i+1}: ").strip() for i in range(n)]

# Input rules
m = int(input("\nEnter number of rules: "))
rules = [input(f"Rule {i+1} (use ^ for AND, => for implies): ").strip() for i in range(m)]

# Input query
query = input("\nEnter the query to prove: ").strip()

print("\nInitial Facts:")
for f in facts:
    print(" ", f)

print("\n--- Forward Chaining Steps ---")
inferred = infer(facts, rules)

print("\nAll inferred facts:")
for f in inferred:
    print(" ", f)

if query in inferred:
    print(f"\n✅ Query '{query}' is proved using Forward Chaining!")
else:
    print(f"\n❌ Query '{query}' cannot be proved.")
