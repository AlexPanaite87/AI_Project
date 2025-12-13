import tkinter as tk
import face as f
from brain import set_difficulty
from glue import set_board_dimension

if __name__ == '__main__':

    set_difficulty(1)
    set_board_dimension(2)
    root = tk.Tk()
    app = f.SudokuUI(root)
    root.mainloop()