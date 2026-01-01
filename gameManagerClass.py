import tkinter as tk
import copy


class GameManager:
    PLAYER=1
    COMPUTER = 2
    def __init__(self, buttons):
        self.turn = self.PLAYER
        self.buttons = buttons # butoanele din interfata
        self.game_matrix = [[0 for _ in range(3)] for _ in range(3)] # matrice de 3 x 3 cu zerouri

    def game_ended(self):
        #cazuri in care castiga cineva
        for i in range(0,3):  # verific liniile daca is de acelas tip mergand pe centru 01 11 21 cu vecinii stanga dreapta
            if(self.game_matrix[i][1] == self.PLAYER or self.game_matrix[i][1]==self.COMPUTER):
                if self.game_matrix[i][1] == self.game_matrix[i][0] and self.game_matrix[i][1] == self.game_matrix[i][2]:
                    return self.PLAYER if self.turn == self.COMPUTER else self.COMPUTER
        for i in range(0, 3):  # verific coloanele, verific [1][0], [1][1], [1][2] si vecinii
            if (self.game_matrix[1][i] == self.PLAYER or self.game_matrix[1][i] == self.COMPUTER):
                if self.game_matrix[1][i] == self.game_matrix[0][i] and self.game_matrix[1][i] == self.game_matrix[2][i]:
                    return self.PLAYER if self.turn == self.COMPUTER else self.COMPUTER

        # verific diagonalele:
        if (self.game_matrix[1][1] == self.PLAYER or self.game_matrix[1][1] == self.COMPUTER):
            if self.game_matrix[0][0] == self.game_matrix[1][1] and self.game_matrix[1][1] == self.game_matrix[2][2]:
                return self.PLAYER if self.turn == self.COMPUTER else self.COMPUTER
            if self.game_matrix[1][1] == self.game_matrix[0][2] and self.game_matrix[1][1] == self.game_matrix[2][0]:
                return self.PLAYER if self.turn == self.COMPUTER else self.COMPUTER

        #daca jocul nu s-a terminat
        for i in range(0,3):
            for j in range(0, 3):
                if self.game_matrix[i][j] != self.COMPUTER and self.game_matrix[i][j] != self.PLAYER:
                    return 0

        #daca jocul s-a terminat cu toate locurile ocupate
        return 3

    def verif_move(self,x,y):
        if self.game_matrix[x][y] == 0:
            return True #mutare valida
        else:
            return False

    def buttonPressed(self, x, y):
        if self.turn == GameManager.COMPUTER:
            if self.verif_move(x,y):
                self.buttons[x][y].configure(text="O")
                self.turn = self.PLAYER
                self.game_matrix[x][y] = GameManager.PLAYER

        else:
            if self.verif_move(x, y):
                self.buttons[x][y].configure(text="X")
                self.turn = GameManager.COMPUTER
                self.game_matrix[x][y] = GameManager.COMPUTER

    def reset(self):
        for x in range(3):  # resetarea textului de pe butoane
            for y in range(3):
                self.game_matrix[x][y] = 0

    # functie care returneaza toate mutarile valide
    def validMoves(self, matrix):
        moves = []
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == 0:
                    moves.append((i,j))
        return moves

    # functie --- alta varianta de la game_ended dar in loc de game_matrix foloseste matrix
    def checkWin(self,matrix):
        # returneaza castigatorul: 1,2 sau 3(remizaa)
        for i in range(3):
            if matrix[i][0] == matrix[i][1] == matrix[i][2] != 0: return matrix[i][0]
            if matrix[0][i] == matrix[1][i] == matrix[2][i] != 0: return matrix[0][i]
        if matrix [0][0] == matrix[1][1] == matrix[2][2] != 0: return matrix[0][0]
        if matrix [0][2] == matrix[1][1] == matrix[2][0] != 0: return matrix[0][2]

        # schema invatata la practica =D
        if all(matrix[i][j] != 0 for i in range(3) for j in range(3)): return 3
        return 0