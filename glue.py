import math
import random
import os
import json
import brain


BOARD_DIMENSION = 4
BLOCK_SIZE = int(math.sqrt(BOARD_DIMENSION))
DIFFICULTY = 1
FILENAME = 'startup.json'


def set_board_dimension(dimension):
    if math.floor(math.sqrt(dimension)) == math.sqrt(dimension):
        BOARD_DIMENSION = dimension
    else:
        BOARD_DIMENSION = input("Set a new board dimension (4, 9, etc): ")


def validate_board(board):
    for row in board:
        nums = [n for n in row if n != 0]
        if len(nums) != len(set(nums)):
            return False

    for col_index in range(BOARD_DIMENSION):
        nums = []
        for row_idx in range(BOARD_DIMENSION):
            val = board[row_idx][col_index]
            if val != 0:
                nums.append(val)
        if len(nums) != len(set(nums)):
            return False

    for r in range(0, BOARD_DIMENSION, BLOCK_SIZE):
        for c in range(0, BOARD_DIMENSION, BLOCK_SIZE):
            nums = []
            for i in range(r, r + BLOCK_SIZE):
                for j in range(c, c + BLOCK_SIZE):
                    val = board[i][j]
                    if val != 0:
                        nums.append(val)
            if len(nums) != len(set(nums)):
                return False

    return True


def create_valid_board_structure():
    board = [[0] * BOARD_DIMENSION for _ in range(BOARD_DIMENSION)]

    for i in range(0, BOARD_DIMENSION, BLOCK_SIZE):
        nums = list(range(1, BOARD_DIMENSION + 1))
        random.shuffle(nums)
        num_index = 0
        for r in range(BLOCK_SIZE):
            for c in range(BLOCK_SIZE):
                board[i + r][i + c] = nums[num_index]
                num_index += 1

    try:
        solved_board = brain.solve_sudoku_forward_checking(board)

        if solved_board is None:
            return board

        board = solved_board
    except Exception as e:
        print(f"An error occurred while generating the board: {e}")
        return board

    total_cells = BOARD_DIMENSION * BOARD_DIMENSION
    if DIFFICULTY == "0":
        remove_percentage = 0.50
    else:
        remove_percentage = 0.80
    cells_to_remove = int(total_cells * remove_percentage)

    while cells_to_remove > 0:
        row = random.randint(0, BOARD_DIMENSION - 1)
        col = random.randint(0, BOARD_DIMENSION - 1)

        if board[row][col] != 0:
            board[row][col] = 0
            cells_to_remove -= 1

    return board


def load_all_boards():
    if not os.path.exists(FILENAME):
        return {}
    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_new_board(board):
    all_data = load_all_boards()
    board_key = f"{BOARD_DIMENSION}x{BOARD_DIMENSION}"

    if board_key not in all_data:
        all_data[board_key] = []

    all_data[board_key].append(board)

    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4)
    except IOError as e:
        print(f"An error occurred while saving the board: {e}")