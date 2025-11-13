def compute_heuristic(board):
    """Number of attacking pairs of queens."""
    h = 0
    n = len(board)
    for i in range(n):
        for j in range(i+1, n):
            if board[i] == board[j] or abs(board[i]-board[j]) == abs(i-j):
                h += 1
    return h

def hill_climbing_swap_nqueens_user_input(n, board):
    """Hill Climbing using swaps starting from a given board."""
    h_current = compute_heuristic(board)
    print(f"Initial board: {board}, h={h_current}")

    while True:
        min_h = h_current
        best_swap = None

        # Try all pairs of columns
        for i in range(n-1):
            for j in range(i+1, n):
                new_board = board.copy()
                new_board[i], new_board[j] = new_board[j], new_board[i]  # Swap
                h_new = compute_heuristic(new_board)

                # Choose best swap (tie → min-subscript)
                if h_new < min_h or (h_new == min_h and (best_swap is None or i < best_swap[0])):
                    min_h = h_new
                    best_swap = (i, j)

        if best_swap is None:
            # No better swap → local minimum
            print(f"Stopped at local minimum: {board}, h={h_current}")
            return board, h_current

        # Perform the best swap
        i, j = best_swap
        board[i], board[j] = board[j], board[i]
        h_current = min_h
        print(f"Swapped columns {i} and {j}, new board: {board}, h={h_current}")

        if h_current == 0:
            print(f"Solution found: {board}")
            return board, h_current

# --- Example: User Input ---
n = int(input("Enter number of queens (N): "))

# Enter initial state as space-separated row numbers for each column
# Example for N=4: 1 3 0 2
initial_state = list(map(int, input(f"Enter initial board (row positions for {n} queens): ").split()))

hill_climbing_swap_nqueens_user_input(n, initial_state)
