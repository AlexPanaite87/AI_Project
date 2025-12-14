import tkinter as tk
from tkinter import messagebox
import glue as g
import brain as b

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Sudoku Solver")
        self.cells = []
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack()

        self.configure_menu()
        self.create_grid_entries()

        self.on_generate_button_click()

    def configure_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.on_generate_button_click)
        game_menu.add_command(label="Solve", command=self.solve_sudoku)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        message = f"Sudoku Solver using Forward Checking Algorithm.\n\nTeam:\n- Sorina (The Brain)\n- Iustina (The Face)\n- Alex (The Glue)"
        messagebox.showinfo("About", message)

    def create_grid_entries(self):
        vcmd = (self.root.register(self.validate_input), '%P')

        for r in range(g.BOARD_DIMENSION):
            row_entries = []
            for c in range(g.BOARD_DIMENSION):
                block_row = r // g.BLOCK_SIZE
                block_col = c // g.BLOCK_SIZE
                is_colored = (block_row + block_col) % 2 == 0
                bg_color = '#e6e6e6' if is_colored else 'white'

                entry = tk.Entry(self.main_frame, width=3, font=('Arial', 20),
                                 justify='center', bg=bg_color, relief='solid', bd=1,
                                 validate='key', validatecommand=vcmd)

                entry.grid(row=r, column=c, padx=1, pady=1, ipady=5)
                row_entries.append(entry)
            self.cells.append(row_entries)

    def validate_input(self, new_value):
        if new_value == "": return True

        if not new_value.isdigit():
            return False

        val = int(new_value)
        return 1 <= val <= g.BOARD_DIMENSION

    def display_grid(self, board):
        for r in range(g.BOARD_DIMENSION):
            for c in range(g.BOARD_DIMENSION):
                entry = self.cells[r][c]
                val = board[r][c]

                entry.config(state='normal')
                entry.delete(0, tk.END)

                if val != 0:
                    entry.insert(0, str(val))
                    entry.config(state='readonly', fg='#170170', readonlybackground=entry.cget('bg'))
                else:
                    entry.config(state='normal', fg='black')

    def get_board_from_ui(self):
        board = []
        for r in range(g.BOARD_DIMENSION):
            row_data = []
            for c in range(g.BOARD_DIMENSION):
                entry = self.cells[r][c]
                text = entry.get()
                if text.isdigit():
                    val = int(text)
                else:
                    val = 0
                row_data.append(val)
            board.append(row_data)
        return board

    def on_generate_button_click(self):
        new_board = g.create_valid_board_structure()
        self.display_grid(new_board)
        g.save_new_board(new_board)

    def solve_sudoku(self):
        current_board = self.get_board_from_ui()

        if not g.validate_board(current_board):
            messagebox.showerror("Error", "Invalid solution! (duplicated elements on rows / columns / blocks)!")
            return
        try:
            solved_board = b.solve_sudoku_forward_checking(current_board)

            if solved_board:
                for r in range(g.BOARD_DIMENSION):
                    for c in range(g.BOARD_DIMENSION):
                        entry = self.cells[r][c]
                        if entry.get() == "":
                            entry.insert(0, str(solved_board[r][c]))
                            entry.config(fg='green')
                messagebox.showinfo("Game Over", "Congratulations, you found the solution!")
            else:
                messagebox.showwarning("Game Over", "No solution found.")
        except Exception as e:
            messagebox.showerror("Critical Error", f"An error occurred in the algorithm: {e}")