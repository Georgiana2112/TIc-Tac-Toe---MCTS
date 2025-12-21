import tkinter as tk
class GameManager:
    PLAYER=1
    COMPUTER = 2
    def __init__(self, buttons):
        self.turn = self.PLAYER
        self.buttons = buttons # butoanele din interfata
        self.game_matrix = [[0 for _ in range(3)] for _ in range(3)] # matrice de 3 x 3 cu zerouri

    def verif_move(self,x,y):
        if self.game_matrix[x][y] == 0:
            return True #mutare valida
        else:
            return False

    # to do: de integrat fct asta pentru mesaj de sfarsit joc
    def game_ended(self):
        for i in range(0,3): # verific liniile daca is de acelas tip mergand pe centru 01 11 21 cu vecinii stanga dreapta
            if self.game_matrix[i][1] == self.game_matrix[i][0] and self.game_matrix[i][1] == self.game_matrix[i][2]:
                return True
        for i in range(0,3): # verific coloanele, verific [1][0], [1][1], [1][2] si vecinii
            if self.game_matrix[1][i] == self.game_matrix[0][i] and self.game_matrix[1][i] == self.game_matrix[2][i]:
                return True
        #verific diagonalele:
        if self.game_matrix[0][0] == self.game_matrix[1][1] and self.game_matrix[1][1] == self.game_matrix[2][2]:
            return True
        if self.game_matrix[1][1] == self.game_matrix[0][2] and self.game_matrix[0][1] == self.game_matrix[2][0]:
            return True
        return False

    def buttonPressed(self, x, y):
        if self.turn == GameManager.COMPUTER:
            if self.verif_move(x,y):
                self.buttons[x][y].config(text="0")
                self.turn = self.PLAYER
                self.game_matrix[x][y] = GameManager.PLAYER
        else:
            if self.verif_move(x, y):
                self.buttons[x][y].config(text="X")
                self.turn = GameManager.COMPUTER
                self.game_matrix[x][y] = GameManager.COMPUTER
