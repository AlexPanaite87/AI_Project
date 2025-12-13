import copy
import glue as g

GRID_SIZE = g.BOARD_DIMENSION
BLOCK_SIZE = g.BLOCK_SIZE


def get_empty_location(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return r, c
    return None


def forward_check(domains, r, c, val):
    for i in range(GRID_SIZE):
        if i != c:
            if val in domains[r][i]:
                domains[r][i].remove(val)
                if not domains[r][i]: return False
        if i != r:
            if val in domains[i][c]:
                domains[i][c].remove(val)
                if not domains[i][c]: return False

    start_row = (r // BLOCK_SIZE) * BLOCK_SIZE
    start_col = (c // BLOCK_SIZE) * BLOCK_SIZE

    for i in range(start_row, start_row + BLOCK_SIZE):
        for j in range(start_col, start_col + BLOCK_SIZE):
            if i == r and j == c:
                continue

            if val in domains[i][j]:
                domains[i][j].remove(val)
                if not domains[i][j]: return False

    return True


def get_initial_domains(board):
    full_domain = set(range(1, GRID_SIZE + 1))
    domains = [[full_domain.copy() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            val = board[r][c]
            if val != 0:
                domains[r][c] = {val}
                if not forward_check(domains, r, c, val):
                    return None
    return domains


def backtrack(board, domains):
    empty_loc = get_empty_location(board)
    if not empty_loc:
        return board

    row, col = empty_loc
    possible_values = list(domains[row][col])
    possible_values.sort()

    for val in possible_values:
        board[row][col] = val
        new_domains = copy.deepcopy(domains)
        new_domains[row][col] = {val}
        if forward_check(new_domains, row, col, val):
            result = backtrack(board, new_domains)
            if result:
                return result
        board[row][col] = 0

    return None


def solve_sudoku_forward_checking(board):
    working_board = [row[:] for row in board]
    initial_domains = get_initial_domains(working_board)

    if initial_domains is None:
        return None

    return backtrack(working_board, initial_domains)