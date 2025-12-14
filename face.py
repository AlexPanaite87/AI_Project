import tkinter as tk
from tkinter import messagebox
import glue as g
import brain as b

GRID_SIZE = g.BOARD_DIMENSION
BLOCK_SIZE = g.BLOCK_SIZE

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = []
        self.configure_menu()

        self.grid_frame = tk.Frame(self.root, padx=10, pady=10)
        self.grid_frame.pack()
        self.create_grid_entries()

        start_board = g.create_valid_board_structure()
        self.display_grid(start_board)

    def configure_menu(self):
        """Menu bar"""
        menu_bar = tk.Menu(self.root)
        game_menu = tk.Menu(menu_bar,tearoff=0)
        game_menu.add_command(label="New Game", command=self.generate_new)
        game_menu.add_command(label="Solve", command=self.solve_sudoku)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu_bar, tearoff = 0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label ="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def exit_app(self):
        """Close the app"""
        self.root.quit()

    def show_about(self):
        """About the app"""
        about_text = "Sudoku Solver 4x4"
        messagebox.showinfo("About Sudoku", about_text)

    def generate_new(self):
        """Generates a new puzzle"""
        new_board = g.create_valid_board_structure()
        self.display_grid(new_board)
        messagebox.showinfo("New Puzzle", "A new Sudoku puzzle has been generated")

    def get_current_grid_state(self):
        grid =[]
        for row in range(GRID_SIZE):
            row_data = []
            for col in range(GRID_SIZE):
                value=self.cells[row][col].get()
                try:
                    row_data.append(int(value))
                except ValueError:
                    row_data.append(0)
            grid.append(row_data)
        return grid

    def solve_sudoku(self):
        current_grid = self.get_current_grid_state()
        solved_board = b.solve_sudoku_forward_checking(current_grid)

        if solved_board:
            self.display_grid(solved_board)
            messagebox.showinfo("Success", "Sudoku solved")
        else:
            messagebox.showerror("Error", "The Sudoku has no valid solution")

    def create_grid_entries(self):
        """Create grids"""
        for row in range(GRID_SIZE):
            row_entries =[]
            for col in range(GRID_SIZE):
                cell_entry = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=('Arial', 18, 'bold'),
                    justify='center',
                    relief='solid',
                    bd=1
                )
                cell_entry.grid(row=row, column = col, padx=1,pady=1,ipadx=5,ipady=5)
                row_entries.append(cell_entry)
            self.cells.append(row_entries)

    def display_grid(self,board):
        """Displays the board values in the Entry widgets and sets initial cells to readonly"""
        self.initial_board = [row[:] for row in board]

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = board[row][col]
                entry=self.cells[row][col]
                entry.config(state='normal')
                entry.delete(0,tk.END)

                if value!= 0:
                    entry.insert(0,str(value))
                    entry.config(state='readonly', readonlybackground = 'lightgray', fg='blue')
                else:
                    entry.config(state='normal', fg='black', readonlybackground ='white', bg='white')
