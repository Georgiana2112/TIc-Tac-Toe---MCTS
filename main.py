import tkinter as tk
from tkinter import messagebox, ttk, Label
import tkinter.font as tkFont

from PIL.ImageChops import offset
from fontTools.misc.py23 import xrange

from util import GameManager


#paleta de culori folosita: https://colorhunt.co/palette/97a87aa8bba3fcf9eaffa239

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("TIC TAC TOE")
        self.root.geometry("890x653")
        self.btn_x_0 = 0
        self.create_widgets()

        self.game_manager = GameManager(self.btn_x_0)

    def create_widgets(self):
        self.root.configure(background="#A8BBA3")
        frame = tk.Frame(
            root,
            width = 675,
            height= 633,
            bg="#FCF9EA",
            highlightthickness = 2,
            highlightbackground = "#97A87A"
        )
        frame.place(x=100,y=10)

        #textul de sus
        font = tkFont.Font(family="Times New Roman", size = 30, weight = "bold")
        main_label = Label(frame, text = 'Tic-Tac-Toe', font = font,fg = "#97A87A", bg ="#FCF9EA")
        main_label.place(x = 350, y = 45,anchor=tk.CENTER)


        self.btn_x_0 = [[0 for x in range(3)] for x in range(3)]
        for x in range(3):
            for y in range(3):
                self.btn_x_0[x][y] = tk.Button(frame) #parinte -> frame

                self.btn_x_0[x][y].config(
                    height = 10,
                    width = 20,
                    bg = '#F7B980',
                    activebackground="#ED985F",
                    relief = tk.FLAT,
                    command = lambda a=x, b=y: self.game_manager.buttonPressed( a, b)
                ) #10 si 20 pentru a fi cat de cat patrate -> se masoara in unitate de text
                self.btn_x_0[x][y].grid(row = x+1, column = y)

                # cele doua o sa difere in caz de e pe prima/ultima linie/coloana
                offset_sus = 5
                offset_jos = 5
                offset_dreapta = 5
                offset_stanga = 5

                if (y==0): # daca e prima coloana
                    offset_stanga = 100
                if(x==0): # daca e pe prima linie
                    offset_sus = 100
                if(y==2):
                    offset_dreapta = 100
                if(x==2):
                    offset_jos = 20
                self.btn_x_0[x][y].grid_configure(padx=(offset_stanga,offset_dreapta), pady=(offset_sus,offset_jos))


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()