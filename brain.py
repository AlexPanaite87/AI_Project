import glue as g


def get_empty_location(board):
    for r in range(g.BOARD_DIMENSION):
        for c in range(g.BOARD_DIMENSION):
            if board[r][c] == 0:
                return r, c
    return None


def forward_check(domains, r, c, val):

    marks = []

    neighbors = set()
    for i in range(g.BOARD_DIMENSION):
        if i != c: neighbors.add((r, i))
        if i != r: neighbors.add((i, c))

    start_row = (r // g.BLOCK_SIZE) * g.BLOCK_SIZE
    start_col = (c // g.BLOCK_SIZE) * g.BLOCK_SIZE

    for i in range(start_row, start_row + g.BLOCK_SIZE):
        for j in range(start_col, start_col + g.BLOCK_SIZE):
            if (i, j) != (r, c):
                neighbors.add((i, j))

    for nr, nc in neighbors:
        if val in domains[nr][nc]:
            domains[nr][nc].remove(val)
            marks.append((nr, nc, val))
            if not domains[nr][nc]:
                return False, marks
    return True, marks

def get_initial_domains(board):
    full_domain = set(range(1, g.BOARD_DIMENSION + 1))
    domains = [[full_domain.copy() for _ in range(g.BOARD_DIMENSION)] for _ in range(g.BOARD_DIMENSION)]

    for r in range(g.BOARD_DIMENSION):
        for c in range(g.BOARD_DIMENSION):
            val = board[r][c]
            if val != 0:
                domains[r][c] = {val}
                valid, _ = forward_check(domains, r, c, val)
                if not valid:
                    return None
    return domains


def backtrack(board, domains):
    empty_location = get_empty_location(board)
    if not empty_location:
        return board

    row, col = empty_location
    possible_values = sorted(list(domains[row][col]))

    for val in possible_values:
        board[row][col] = val
        valid, marks = forward_check(domains, row, col, val)
        if valid:
            result = backtrack(board, domains)
            if result:
                return result
        for (marked_row, marked_col, marked_val) in marks:
            domains[marked_row][marked_col].add(marked_val)
        board[row][col] = 0

    return None


def solve_sudoku_forward_checking(board):
    working_board = [row[:] for row in board]
    initial_domains = get_initial_domains(working_board)

    if initial_domains is None:
        return None

    return backtrack(working_board, initial_domains)