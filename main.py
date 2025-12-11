import tkinter as tk
from tkinter import messagebox
import glue as g

GRID_SIZE = g.BOARD_DIMENSION
BLOCK_SIZE = g.BLOCK_SIZE

class SudokuUI:
    def __init__(self, root, start_board, generate_callback):
        self.root = root
        self.root.title("Sudoku")
        self.generate_callback = generate_callback
        self.cells = {}

        self.configure_menu()

    def configure_menu(self):
        """Creeaza si seteaza bara de meniu"""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu = menu_bar)

        game_menu = tk.Menu(menu_bar,tearoff=0)
        game_menu.add_command(label="New Game", command=self.on_generate_btn_click)
        game_menu.add_command(label="Solve", command=self.solve_sudoku)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu_bar, tearoff = 0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label ="Help", menu=help_menu)

    def exit_app(self):
        """"Inchide aplicatia"""
        self.root.quit()

    def show_about(self):
        """Despre aplicatie"""
        about_text = "Sudoku Solver 4x4"
        messagebox.showinfo("Despre Sudoku", about_text)

    def on_generate_btn_click(self):
        messagebox.showinfo("Trebuie implementata")

    def solve_sudoku(self):
        messagebox.showinfo("Trebuie implementata")


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

    app = SudokuUI(root, start_board, handle_generate_new)
    root.mainloop()


if __name__ == '__main__':
    main()