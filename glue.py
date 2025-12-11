import json
import math
import random
import os

BOARD_DIMENSION = 4
BLOCK_SIZE = int(math.sqrt(BOARD_DIMENSION))
FILENAME = 'startup.json'

def validate_board(board):
    for row in board:
        nums = [n for n in row if n != 0]
        if len(nums) != len(set(nums)):
            return False

    for col_idx in range(BOARD_DIMENSION):
        nums = []
        for row_idx in range(BOARD_DIMENSION):
            val = board[row_idx][col_idx]
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
    while True:
        board = [[0] * BOARD_DIMENSION for _ in range(BOARD_DIMENSION)]

        for i in range(BOARD_DIMENSION):
            j = random.randint(0, BOARD_DIMENSION - 1)
            val = random.randint(1, BOARD_DIMENSION)
            board[i][j] = val

        if validate_board(board):
            return board

def load_all_boards():
    if not os.path.exists(FILENAME):
        return {}

    try:
        with open(FILENAME, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        return {}


def save_new_board(board):
    all_data = load_all_boards()

    board_key = f"{BOARD_DIMENSION}x{BOARD_DIMENSION}"
    if board_key not in all_data:
        all_data[board_key] = []
    all_data[board_key].append(board)

    try:
        with open(FILENAME, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error: {e}")