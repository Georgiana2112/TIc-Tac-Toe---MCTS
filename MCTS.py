import math
import sys
import copy
import random
#from gameManagerClass import GameManager

class Node:
    def __init__(self, matrix, player_turn, parent=None): # vechi :(self, board,parent):
        #self.board = board
        self.matrix = matrix
        self.parent = parent #None # posibil sa trebuiasca o lista de parinti
        self.wins = 0
        #self.draws = 0 # egaluri

        # astea sunt ce zic ca trebuie in completare, ptr algoritm
        self.visits = 0
        self.children = {} # ptr arbore
        self.player_turn = player_turn # cine urmeaza sa mute


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
        if self.visits == 0: # daca nodul nu a fost vizitat -> uct = inf
            return float('inf')
            #return sys.maxint - 1 # sau float('inf')

        # return (self.wins + 0.5 * self.draws) / self.visits + c * math.sqrt(math.log(self.parent.visits)/self.visits) # de verificat daca e corect
        # posibil sa trebuiasca in functie de mai multi parinti -> mai multe iteratii
        return (self.wins / self.visits) + c*math.sqrt(math.log(self.parent.visits)/self.visits)
        # mai sus e alta formula gasita care se leaga de mai multe noduri

def predictie(game_manager, noSimulations = 1000):
    matrix = copy.deepcopy(game_manager.game_matrix)# copie a matricii de joc
    root_node = Node(matrix,game_manager.COMPUTER) #radacina arborelui

    for _ in range(noSimulations):
        node = root_node
        matriceSimulare = copy.deepcopy(matrix)
        playerCurent = game_manager.COMPUTER

        # selectie
        while node.children:
            move,node = max(node.children.items(), key=lambda x:x[1].calculate_uct()) # aleg copilul cu uct maxim
            matriceSimulare[move[0]][move[1]] = playerCurent #aplica mutarea in simulare
            playerCurent = 1 if playerCurent == 2 else 2

        #expansiune
        winner = game_manager.checkWin(matriceSimulare) # daca jocul nu s-a terminat
        if winner == 0:
            moves = game_manager.validMoves(matriceSimulare)
            for m in moves:
                mat = copy.deepcopy(matriceSimulare)
                mat[m[0]][m[1]] = playerCurent
                playerUrmator = 1 if playerCurent == 2 else 2
                node.children[m] = Node(mat,playerUrmator,parent=node) # creaza toti copiii posibili

            # copil random ptr rollout
            move,node = random.choice(list(node.children.items()))
            matriceSimulare[move[0]][move[1]] = playerCurent
            playerCurent = 1 if playerCurent == 2 else 2

        #rollout
        while game_manager.checkWin(matriceSimulare) == 0:
            moves = game_manager.validMoves(matriceSimulare)
            m=random.choice(moves)
            matriceSimulare[m[0]][m[1]] = playerCurent
            playerCurent = 1 if playerCurent == 2 else 2

        #backpropagation
        winner_sim = game_manager.checkWin(matriceSimulare)
        nod_temporar = node
        while nod_temporar:
            nod_temporar.visits += 1
            if winner_sim == game_manager.COMPUTER:
                nod_temporar.wins = nod_temporar.wins + 1
            elif winner_sim == 3:
                nod_temporar.wins = nod_temporar.wins + 0.5
            nod_temporar = nod_temporar.parent

    print("\n________VERIFICARE VALORI MCTS_________")
    for move, n in root_node.children.items():
        win_rate = (n.wins / n.visits) * 100 if n.wins > 0 else 0
        print(f"Mutare {move}: Vizite: {n.visits}, Rata castig: {win_rate:.1f}%")

    # se returneaza mutarea cu cele mai multe vizitari, adica cea mai sigura
    best_move = max(root_node.children.items(), key=lambda x: x[1].visits)
    print(f"Best move: {best_move[0]}")

    return best_move[0]