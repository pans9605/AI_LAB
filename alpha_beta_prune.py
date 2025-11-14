# Alpha-Beta Pruning Implementation

# function for alpha-beta pruning
def alpha_beta(node, depth, alpha, beta, isMax, tree):
    # If this node is a leaf node
    if depth == 0 or node not in tree:
        return node   # leaf node value itself

    if isMax:
        best = float('-inf')

        print(f"MAX node at {node}, alpha={alpha}, beta={beta}")

        for child in tree[node]:
            val = alpha_beta(child, depth - 1, alpha, beta, False, tree)
            best = max(best, val)
            alpha = max(alpha, best)

            print(f" MAX visiting child {child}, value={val}, updated alpha={alpha}")

            if beta <= alpha:
                print(f"  PRUNED remaining children of {node} (beta={beta}, alpha={alpha})")
                break
        return best

    else:
        best = float('inf')

        print(f"MIN node at {node}, alpha={alpha}, beta={beta}")

        for child in tree[node]:
            val = alpha_beta(child, depth - 1, alpha, beta, True, tree)
            best = min(best, val)
            beta = min(beta, best)

            print(f" MIN visiting child {child}, value={val}, updated beta={beta}")

            if beta <= alpha:
                print(f"  PRUNED remaining children of {node} (beta={beta}, alpha={alpha})")
                break
        return best


# -----------------------------
# Example Tree
# -----------------------------
# You can modify the tree values based on your question/ppt.

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [3, 5],       # leaf nodes
    'E': [6, 9],
    'F': [1, 2],
    'G': [0, -1]
}

# Run Alpha-Beta Pruning from root A
print("\nStarting Alpha-Beta Pruning...\n")
root_value = alpha_beta('A', depth=3, alpha=float('-inf'), beta=float('inf'), isMax=True, tree=tree)

print("\nFinal Value at Root A =", root_value)
