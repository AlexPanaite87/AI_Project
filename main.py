import tkinter as tk
import glue as g

class MockUI:
    def __init__(self, root, start_board, generate_callback):
        self.root = root
        self.root.title("Sudoku")
        self.generate_callback = generate_callback
        self.row_labels = []

        tk.Label(root, text="Current Board (from glue.py):").pack()

        for row in start_board:
            lbl = tk.Label(root, text=str(row), font=("Consolas", 12))
            lbl.pack()
            self.row_labels.append(lbl)

        tk.Button(root, text="New Board", command=self.on_generate_btn_click).pack(pady=20)

    def on_generate_btn_click(self):
        new_board = self.generate_callback()
        self.update_display(new_board)

    def update_display(self, board):
        for i, row in enumerate(board):
            self.row_labels[i].config(text=str(row))


def main():
    root = tk.Tk()
    root.geometry("400x400")

    all_data = g.load_all_boards()
    key = f"{g.BOARD_DIMENSION}x{g.BOARD_DIMENSION}"
    existing_boards = all_data.get(key, [])

    if existing_boards:
        start_board = existing_boards[0]
        print("Main: Loaded board from JSON!")
    else:
        start_board = g.create_valid_board_structure()
        g.save_new_board(start_board)
        print("Main: Empty JSON, generated a new board!")

    def handle_generate_new():
        new_board = g.create_valid_board_structure()
        g.save_new_board(new_board)
        return new_board

    app = MockUI(root, start_board, handle_generate_new)
    root.mainloop()


if __name__ == '__main__':
    main()