import tkinter as tk
from tkinter import messagebox, ttk, Label

from fontTools.misc.py23 import xrange


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Retele neuronale - Regiuni de decizie")
        self.root.geometry("900x618")
        self.canvas_size = 200
        self.create_widgets()

    def create_widgets(self):
        #definerea fiecarui element
        # main_label = Label(root, text = 'X si 0')
        btn = [[0 for x in range(3)] for x in range(3)]
        for x in range(3):
            for y in range(3):
                btn[x][y] = tk.Button(root)
                btn[x][y].config(height = 10, width = 20,bg = 'misty rose',activebackground="lavender")
                btn[x][y].grid(row = x, column = y)
                # if (x == 0 or y==0):
                #     btn[x][y].grid_configure(padx = (20,5), pady = (20,5))
                # else:
                btn[x][y].grid_configure(padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()