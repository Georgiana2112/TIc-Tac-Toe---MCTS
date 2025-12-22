import tkinter as tk
from tkinter import messagebox, ttk, Label
import tkinter.font as tkFont


from gameManagerClass import GameManager


#paleta de culori folosita: https://colorhunt.co/palette/97a87aa8bba3fcf9eaffa239

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("TIC TAC TOE")
        self.root.geometry("890x653")
        self.root.resizable(False, False)
        self.btn_x_0 = 0
        self.create_widgets()
        self.game_manager = GameManager(self.btn_x_0)

    def on_btn_press(self, x, y):
        self.game_manager.buttonPressed( x, y)
        winner = self.game_manager.game_ended()
        if (winner != 0):
            self.show_game_over_window(winner) #1 - PLAYER, 2 - COMPUTER, 3 - EGALITATE

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
        frame.place(x=100,y=30)

        #textul de sus
        font = tkFont.Font(family="Times New Roman", size = 30, weight = "bold")
        main_label = Label(frame, text = 'Tic-Tac-Toe', font = font,fg = "#97A87A", bg ="#FCF9EA")
        main_label.place(x = 350, y = 45,anchor=tk.CENTER)


        self.btn_x_0 = [[0 for x in range(3)] for x in range(3)]
        for x in range(3):
            for y in range(3):
                self.btn_x_0[x][y] = tk.Button(frame) #parinte -> frame

                self.btn_x_0[x][y].config(
                    font=("Helvetica", 36,"bold"),
                    width=5,
                    height=2,
                    bg = '#F7B980',
                    fg = '#FCF9EA',
                    activebackground="#ED985F",
                    relief = tk.FLAT,
                    command = lambda a=x, b=y: self.on_btn_press( a, b)
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

    def show_game_over_window(self, winner):
        win = tk.Toplevel(self.root)
        win.title("")
        win.geometry("300x180")
        win.configure(bg="#FCF9EA")
        win.resizable(False, False)


        if winner == 1: # a castigat jucatorul
            msg = "PLAYER WON"
        elif winner == 2: # a castigat monte carlo
            msg = "COMPUTER WON"
        elif winner == 3: # egal
            msg = "It's a tie!"

        Font = tkFont.Font(family="Helvetica", size = 20, weight="bold")
        label = tk.Label(win, text=msg,  bg="#FCF9EA",fg="#97A87A",font=Font)
        label.pack(pady = (30,5))

        # btn pentru joc nou
        btn_restart = tk.Button(win, text="New Game", width=10, command=lambda: self.restart_game(win))
        btn_restart.pack(side=tk.LEFT, padx=20, pady=10)
        btn_restart.config( bg = '#F7B980',
                            fg = 'black',
                            activebackground="#ED985F",
                            relief=tk.FLAT,
                            )
        # quit
        btn_quit = tk.Button(win, text="Quit", width=10, command=self.root.destroy)
        btn_quit.pack(side=tk.RIGHT, padx=20, pady=10)
        btn_quit.config(bg='#F7B980',
                       fg='black',
                       activebackground="#ED985F",
                       relief=tk.FLAT,
                       )
    def restart_game(self, window):
        window.destroy()  # inchiderea ferestrei cu mesaj de final
        for x in range(3):# resetarea textului de pe butoane
            for y in range(3):
                self.btn_x_0[x][y].configure(text="")

        self.game_manager.reset()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()