import tkinter as tk
from tkinter import messagebox
import glue as g
import brain as b

class StartScreen:
    def __init__(self, root):
        """Initializarea ecranului principal pentru alegerea dificulatii si a dimensiunii"""
        self.root = root
        root.title("Select Sudoku settings")

        self.frame = tk.Frame(root,padx=20, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="Choose dimension and difficulty:", font=('Arial', 14)).pack(pady=10)
        self.dimension_var = tk.IntVar(value=4)
        tk.Radiobutton(self.frame, text="4x4",variable=self.dimension_var,value=4, font=('Arial', 12), padx=10, pady=5).pack(pady=5)
        tk.Radiobutton(self.frame, text="9x9",variable=self.dimension_var, value =9, font=('Arial', 12), padx=10, pady=5).pack(pady=5)

        self.difficulty_var = tk.IntVar(value=0)
        tk.Radiobutton(self.frame, text="Easy", variable=self.difficulty_var, value=0, font=('Arial', 12), padx=10, pady=5).pack(pady=5)
        tk.Radiobutton(self.frame, text="Hard", variable=self.difficulty_var, value=1, font=('Arial', 12),  padx=10, pady=5).pack(pady=5)

        tk.Button(self.frame, text="Start Game", command=self.start_game, font=('Arial', 12), padx=10, pady=5).pack(pady=15)

    def start_game(self):
        """Setarea variabilelor si inceperea jocului"""
        dimension = self.dimension_var.get()
        difficulty=self.difficulty_var.get()
        g.set_dimension(dimension)
        g.set_difficulty(difficulty)

        self.frame.destroy()
        SudokuUI(self.root)


class SudokuUI:
    def __init__(self, root):
        """Initializarea tabelului principal pentru joc"""
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
        """Verificarea inputului(daca cifra pe care o punem este valida pentru jocul respectiv)"""
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
        """Bara de meniu"""
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
        """Inchiderea aplicatiei"""
        self.root.quit()

    def show_about(self):
        """Despre aplicatie"""
        about_text = "Sudoku Solver using Forward Checking Algorithm.\n\nTeam:\n- Sorina (The Brain)\n- Iustina (The Face)\n- Alex (The Glue)"
        messagebox.showinfo("About Sudoku", about_text)

    def get_current_grid_state(self):
        """Functie ajutatoare - ia toate valorile(atat cele generate initial, cat si cele scrise de utilizator) si le returneaza sub forma de matrice pentru verificarile urmatoare """
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
        """Rezolvarea jocului curent automat"""
        current_grid = self.get_current_grid_state()
        if not g.validate_board(current_grid):
            messagebox.showerror("Error", "Invalid solution!")
            return
        try:
            solved_board = b.solve_sudoku_forward_checking(current_grid)
            if solved_board:
                for row in range(g.BOARD_DIMENSION):
                    for col in range(g.BOARD_DIMENSION):
                        entry = self.cells[row][col]
                        if entry.get() == "":
                            entry.insert(0,str(solved_board[row][col]))
                            entry.config(fg="green", state='readonly',readonlybackground=entry.cget('bg'))
                messagebox.showinfo("Success", "Sudoku solved")
            else:
                messagebox.showerror("Error", "The Sudoku has no valid solution")
        except ValueError:
            messagebox.showerror("Error")

    def create_grid_entries(self):
        """Desenarea casutelor pe ecran si asezarea acestora"""
        for row in range(g.BOARD_DIMENSION):
            row_entries =[]
            for col in range(g.BOARD_DIMENSION):
                block_row = row // g.BLOCK_SIZE
                block_col = col // g.BLOCK_SIZE
                if (block_row + block_col)%2 == 0:
                    bg_color = 'lightgray'
                else:
                    bg_color = 'white'

                cell_entry = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=('Arial', 18, 'bold'),
                    justify='center',
                    relief='solid',
                    bg=bg_color,
                    bd=1,
                    validate='key',
                    validatecommand=self.validate
                )
                cell_entry.grid(row=row, column = col, padx=1,pady=1,ipadx=5,ipady=5)
                row_entries.append(cell_entry)
            self.cells.append(row_entries)

    def display_grid(self,board):
        """Afisarea numerelor si blocarea casutelor care au fost completate initial"""
        for row in range(g.BOARD_DIMENSION):
            for col in range(g.BOARD_DIMENSION):
                entry = self.cells[row][col]
                value = board[row][col]
                entry.config(state='normal')
                entry.delete(0,tk.END)

                if value!= 0:
                    entry.insert(0,str(value))
                    entry.config(state='readonly', readonlybackground = entry.cget('bg'), fg='blue')
                else:
                    entry.config(state='normal', fg='black')

    def start_predefined_game(self,dimension, difficulty):
        """Reincarcarea interfetei cu noile setari alese din meniu(dimensiunea si dificultatea jocului)"""
        g.set_dimension(dimension)
        g.set_difficulty(difficulty)
        self.reload_ui()

    def reload_ui(self):
        """Reconstruirea tabelului si generarea unui nou joc"""
        self.grid_frame.destroy()
        self.grid_frame = tk.Frame(self.root, padx=10,pady=10)
        self.grid_frame.pack()
        self.cells =[]
        self.create_grid_entries()
        new_board=g.create_valid_board_structure()
        self.display_grid(new_board)
