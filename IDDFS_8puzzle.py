from copy import deepcopy

# Possible moves for the blank tile
moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

def find_blank(state):
    """Find position of blank (0)."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def possible_moves(state):
    """Return all possible states after moving the blank."""
    i, j = find_blank(state)
    neighbors = []

    for move, (di, dj) in moves.items():
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = deepcopy(state)
            new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
            neighbors.append(new_state)
    return neighbors

def goal_test(state, goal):
    return state == goal

def dls(state, goal, limit, depth=0, path=[]):
    """Depth-Limited Search."""
    path = path + [state]
    if goal_test(state, goal):
        print(f"Goal found at depth {depth}!")
        print("Path to solution:")
        for p in path:
            for row in p:
                print(row)
            print("-----")
        return True
    if limit == 0:
        return False

    for neighbor in possible_moves(state):
        if dls(neighbor, goal, limit - 1, depth + 1, path):
            return True
    return False

def iddfs(start, goal, max_depth=50):
    """Iterative Deepening DFS."""
    for limit in range(max_depth):
        print(f"🔹 Searching at depth limit = {limit}")
        if dls(start, goal, limit):
            print("Goal reached!")
            return
    print("Goal not found within depth limit.")

# --- User Input ---
print("Enter the initial state (3x3), use 0 for blank, row by row):")
initial_state = []
for i in range(3):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    initial_state.append(row)

print("Enter the goal state (3x3), use 0 for blank, row by row):")
goal_state = []
for i in range(3):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    goal_state.append(row)

iddfs(initial_state, goal_state)
