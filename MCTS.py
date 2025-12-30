import math
import sys


class Node:
    def __init__(self, board,parent):
        self.board = board
        self.parent = None # posibil sa trebuiasca o lista de parinti
        self.wins = 0
        self.n = 0
        self.draws = 0 # egaluri
    def generate_valid_moves(self): #genereaza o lista de mutari valide
        valid_moves = []
        for i in range(0,3):
            for j in range(0, 3):
                if self.board[i][j] == 0:
                    valid_moves.append((i,j))
        return valid_moves

    # wins - numarul de victorii pentru nodul curent dupa a i-a mutare
    # ni - numarul de simulari pentru nodul curent dupa a i-a mutare
    # Ni - numarul total de simulari după a i-a miscare executata de nodul parinte al nodului curent
    # c - parametru de explorare in teoretie e sqrt(2), i se poate da si alta valoare
    def calculate_uct(self,c = math.sqrt(2)):
        if self.n == 0: # daca nodul nu a fost vizitat -> uct = inf
            return sys.maxint - 1

        return (self.wins + 0.5 * self.draws) / self.n + c * math.sqrt(math.log(self.parent.n)/self.n) # de verificat daca e corect
        # posibil sa trebuiasca in functie de mai multi parinti -> mai multe iteratii