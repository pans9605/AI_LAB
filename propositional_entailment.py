import itertools
import re

# --- Utility functions ---

def normalize_expr(expr):
    """Convert English logic words to Python syntax safely."""
    expr = expr.strip().lower()
    expr = expr.replace("(", " ( ").replace(")", " ) ")

    # Handle 'implies' manually: A implies B -> (not A or B)
    # Split step by step to avoid cutting inside 'not q'
    parts = expr.split(" implies ")
    if len(parts) == 2:
        left, right = parts
        expr = f"(not ({left.strip()}) or ({right.strip()}))"

    # Handle 'equivalent': A equivalent B -> (A == B)
    parts = expr.split(" equivalent ")
    if len(parts) == 2:
        left, right = parts
        expr = f"(({left.strip()}) == ({right.strip()}))"

    # Basic replacements
    expr = expr.replace(" and ", " and ")
    expr = expr.replace(" or ", " or ")
    expr = expr.replace(" not ", " not ")

    # Replace booleans if user ever types them
    expr = expr.replace("true", "True").replace("false", "False")

    return expr.strip()


def eval_expr(expr, values):
    """Evaluate a logical expression under given truth assignments."""
    expr = normalize_expr(expr)
    # Replace variable names with their truth values
    for var, val in values.items():
        expr = re.sub(rf"\b{var}\b", str(val), expr)
    return eval(expr)


def extract_vars(sentences):
    """Find all propositional variables."""
    vars = set()
    for s in sentences:
        for token in re.findall(r"\b[a-zA-Z]\w*\b", s):
            if token not in ["and", "or", "not", "implies", "equivalent", "true", "false"]:
                vars.add(token)
    return sorted(vars)


# --- Main program ---

print("Enter KB sentences separated by commas.")
print("Use words: and, or, not, implies, equivalent")

kb_input = input("KB = ").strip()
sentences = [s.strip() for s in kb_input.split(",")]

query = input("Enter query (α) = ").strip()

variables = extract_vars(sentences + [query])
print(f"\nVariables found: {variables}\n")

entails = True
for combo in itertools.product([False, True], repeat=len(variables)):
    values = dict(zip(variables, combo))
    kb_value = all(eval_expr(s, values) for s in sentences)
    alpha_value = eval_expr(query, values)

    if kb_value and not alpha_value:
        entails = False
        print(f"Counterexample: {values} — KB=True, α=False")

if entails:
    print("\nKB entails α (KB ⊨ α)")
else:
    print("\nKB does NOT entail α (KB ⊭ α)")
