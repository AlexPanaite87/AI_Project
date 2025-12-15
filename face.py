import tkinter as tk
from tkinter import messagebox
import glue as g
import brain as b

class StartScreen:
    def __init__(self, root):
        self.root = root
        root.title("Select Sudoku size:")

        self.frame = tk.Frame(root,padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="Choose dimension and difficulty:", font=('Arial', 14)).pack(pady=10)
        self.start_menu_button = tk.Menubutton(self.frame, text="Start game", relief=tk.RAISED, font=('Arial',12), padx=10, pady=5,direction='below')
        self.start_menu_button.pack(pady=20)
        self.start_menu = tk.Menu(self.start_menu_button, tearoff=0)
        self.start_menu_button.config(menu=self.start_menu)

        self.start_menu.add_command(label="4x4(Easy)", command=lambda:self.start_game(4,0))
        self.start_menu.add_command(label="4x4(Hard)", command=lambda: self.start_game(4, 1))
        self.start_menu.add_command(label="9x9(Easy)", command=lambda: self.start_game(9, 0))
        self.start_menu.add_command(label="9x9(Hard)", command=lambda: self.start_game(9, 1))

    def start_game(self, dimension, difficulty):
        g.set_dimension(dimension)
        g.set_difficulty(difficulty)
        self.frame.destroy()
        SudokuUI(self.root)


class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.cells = []
        self.configure_menu()

        self.grid_frame = tk.Frame(self.root, padx=10, pady=10)
        self.grid_frame.pack()

        self.validate=(self.root.register(self.validate_input), '%P')
        self.create_grid_entries()

        start_board = g.create_valid_board_structure()
        self.display_grid(start_board)

    def validate_input(self,new_value):
        if new_value == "":
            return True
        try:
            value = int(new_value)
            if value < 1 or value > g.BOARD_DIMENSION:
                return  False
            if len(new_value) != 1:
                return False
            return True
        except ValueError:
            return False

    def configure_menu(self):
        """Menu bar"""
        menu_bar = tk.Menu(self.root)
        game_menu = tk.Menu(menu_bar,tearoff=0)

        new_game_menu = tk.Menu(game_menu, tearoff=0)
        new_game_menu.add_command(label="4x4(Easy)", command=lambda: self.start_predefined_game(4, 0))
        new_game_menu.add_command(label="4x4(Hard)", command=lambda: self.start_predefined_game(4, 1))
        new_game_menu.add_command(label="9x9(Easy)", command=lambda: self.start_predefined_game(9, 0))
        new_game_menu.add_command(label="9x9(Hard)", command=lambda: self.start_predefined_game(9, 1))
        game_menu.add_cascade(label="New Game", menu=new_game_menu)

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
        about_text = "Sudoku Solver using Forward Checking Algorithm.\n\nTeam:\n- Sorina (The Brain)\n- Iustina (The Face)\n- Alex (The Glue)"
        messagebox.showinfo("About Sudoku", about_text)

    def generate_new(self):
        """Generates a new puzzle"""
        new_board = g.create_valid_board_structure()
        self.display_grid(new_board)
        messagebox.showinfo("New Puzzle", "A new Sudoku puzzle has been generated")

    def get_current_grid_state(self):
        grid =[]
        for row in range(g.BOARD_DIMENSION):
            row_data = []
            for col in range(g.BOARD_DIMENSION):
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
        for row in range(g.BOARD_DIMENSION):
            row_entries =[]
            for col in range(g.BOARD_DIMENSION):
                if col % g.BLOCK_SIZE == 0:
                    left_border = 5
                else:
                    left_border = 1

                if row % g.BLOCK_SIZE == 0:
                    top_border = 5
                else:
                    top_border = 1

                if col == g.BOARD_DIMENSION -1:
                    right_border = 5
                else:
                    right_border = 1

                if row == g.BOARD_DIMENSION -1:
                    bottom_border = 5
                else:
                    bottom_border = 1

                cell_entry = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=('Arial', 18, 'bold'),
                    justify='center',
                    relief='solid',
                    bd=1,
                    validate='key',
                    validatecommand=self.validate
                )
                cell_entry.grid(row=row, column = col, padx=(left_border, right_border),pady=(top_border,bottom_border),ipadx=5,ipady=5)
                row_entries.append(cell_entry)
            self.cells.append(row_entries)

    def display_grid(self,board):
        """Displays the board values in the Entry widgets and sets initial cells to readonly"""
        self.initial_board = [row[:] for row in board]

        for row in range(g.BOARD_DIMENSION):
            for col in range(g.BOARD_DIMENSION):
                value = board[row][col]
                entry=self.cells[row][col]
                entry.config(state='normal',bg='white',fg='black')
                entry.delete(0,tk.END)

                if value!= 0:
                    entry.insert(0,str(value))
                    entry.config(state='readonly', readonlybackground = 'lightgray', fg='blue')
                else:
                    entry.config(state='normal', fg='black', readonlybackground ='white', bg='white')

    def start_predefined_game(self,dimension, difficulty):
        g.set_dimension(dimension)
        g.set_difficulty(difficulty)
        self.reload_ui()

    def reload_ui(self):
        self.grid_frame.destroy()
        self.grid_frame = tk.Frame(self.root, padx=10,pady=10)
        self.grid_frame.pack()
        self.cells =[]
        self.create_grid_entries()
        new_board=g.create_valid_board_structure()
        self.display_grid(new_board)
