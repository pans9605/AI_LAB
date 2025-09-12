import heapq

# ----------- Heuristic 1: Misplaced Tiles -----------
def misplaced_tiles(state, goal):
    count = 0
    for i in range(len(state)):
        if state[i] != '0' and state[i] != goal[i]:
            count += 1
    return count

# ----------- Heuristic 2: Manhattan Distance -----------
def manhattan_distance(state, goal):
    distance = 0
    for i, val in enumerate(state):
        if val != '0':
            goal_index = goal.index(val)
            x1, y1 = divmod(i, 3)          # current row, col
            x2, y2 = divmod(goal_index, 3) # goal row, col
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# ----------- A* Algorithm -----------
def a_star(start, goal, heuristic):
    # priority queue (f, state, g, path)
    queue = []
    heapq.heappush(queue, (0, start, 0, []))
    visited = set()

    while queue:
        f, state, g, path = heapq.heappop(queue)

        if state == goal:
            return path   # solved!

        if state in visited:
            continue
        visited.add(state)

        # Find the blank (0)
        idx = state.index('0')
        x, y = divmod(idx, 3)

        # Possible moves
        moves = {
            "Up": (x - 1, y),
            "Down": (x + 1, y),
            "Left": (x, y - 1),
            "Right": (x, y + 1)
        }

        for move, (nx, ny) in moves.items():
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_idx = nx * 3 + ny
                new_state = list(state)
                # swap blank with the target tile
                new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
                new_state = ''.join(new_state)

                if new_state not in visited:
                    h = heuristic(new_state, goal)
                    heapq.heappush(queue, (g + 1 + h, new_state, g + 1, path + [move]))

    return None  # No solution found

# ----------- Test Both Heuristics -----------
if __name__ == "__main__":
    start = "724506831"   # Example start state
    goal = "123456780"    # Goal state

    print("Start State:", start)
    print("Goal State :", goal)

    print("\nUsing Misplaced Tiles Heuristic:")
    path1 = a_star(start, goal, misplaced_tiles)
    print("Moves:", path1)
    print("Steps:", len(path1) if path1 else -1)

    print("\nUsing Manhattan Distance Heuristic:")
    path2 = a_star(start, goal, manhattan_distance)
    print("Moves:", path2)
    print("Steps:", len(path2) if path2 else -1)
