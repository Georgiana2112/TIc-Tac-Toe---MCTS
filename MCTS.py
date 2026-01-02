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



    # wins - numarul de victorii pentru nodul curent dupa a i-a mutare
    # ni - numarul de simulari pentru nodul curent dupa a i-a mutare
    # Ni - numarul total de simulari după a i-a miscare executata de nodul parinte al nodului curent
    # c - parametru de explorare in teoretie e sqrt(2), i se poate da si alta valoare
    def calculate_uct(self,c = math.sqrt(2)):
        if self.visits == 0: # daca nodul nu a fost vizitat -> uct = inf
            return float('inf')

        return (self.wins / self.visits) + c*math.sqrt(math.log(self.parent.visits)/self.visits)


def gaseste_mutare_critica(game_manager, matrix, player_id):
    # verificare daca un jucator are o mutare prin care poate castiga imediat
    moves = game_manager.validMoves(matrix)
    for m in moves:
        matrice_temporara = copy.deepcopy(matrix)
        matrice_temporara[m[0]][m[1]] = player_id
        if game_manager.checkWin(matrice_temporara) == player_id:
            return m
    return None


def selectie(node, matriceSimulare,playerCurent):
    while node.children:
        move, node = max(node.children.items(), key=lambda x: x[1].calculate_uct())  # aleg copilul cu uct maxim
        matriceSimulare[move[0]][move[1]] = playerCurent  # aplica mutarea in simulare
        playerCurent = 1 if playerCurent == 2 else 2
    return node, matriceSimulare, playerCurent


def expansiune(game_manager,matriceSimulare,playerCurent,node):
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
    return node, matriceSimulare, playerCurent


def rollout(game_manager, matriceSimulare,playerCurent):
    while game_manager.checkWin(matriceSimulare) == 0:
        moves = game_manager.validMoves(matriceSimulare)
        m_win = gaseste_mutare_critica(game_manager, matriceSimulare, playerCurent)
        if m_win:
            m = m_win
        else:
            m = random.choice(moves)
        matriceSimulare[m[0]][m[1]] = playerCurent
        playerCurent = 1 if playerCurent == 2 else 2
    return matriceSimulare, playerCurent


def backpropagation(game_manager,matriceSimulare,node):
    winner_sim = game_manager.checkWin(matriceSimulare)
    nod_temporar = node
    while nod_temporar:
        nod_temporar.visits += 1
        if winner_sim == game_manager.COMPUTER:
            nod_temporar.wins = nod_temporar.wins + 1
        elif winner_sim == 3: # daca e egal
            nod_temporar.wins = nod_temporar.wins + 0.5
        # else:
        #     nod_temporar.wins = nod_temporar.wins - 0.25 #temporar
        nod_temporar = nod_temporar.parent


def predictie(game_manager, noSimulations = 1000):
    #matrix = copy.deepcopy(game_manager.game_matrix)# copie a matricii de joc
    matrix = game_manager.game_matrix
    win_move = gaseste_mutare_critica(game_manager, matrix, game_manager.COMPUTER)
    if win_move:
        print("A fost gasita o mutare castigatoare")
        return win_move

    # logica de blocare a jucatorului
    blocare = gaseste_mutare_critica(game_manager, matrix, game_manager.PLAYER)
    if blocare:
        print("Trebuie blocat player-ul")
        return blocare

    root_node = Node(copy.deepcopy(matrix),game_manager.COMPUTER) #radacina arborelui

    if all(cell == 0 for row in matrix for cell in row):
        # tabla e goala, extind toate mutarile posibile AI
        moves = game_manager.validMoves(matrix)
        for m in moves:
            mat = copy.deepcopy(matrix)
            mat[m[0]][m[1]] = game_manager.COMPUTER
            playerUrmator = game_manager.PLAYER
            root_node.children[m] = Node(mat, playerUrmator, parent=root_node)

    for _ in range(noSimulations):
        node = root_node
        matriceSimulare = copy.deepcopy(matrix)
        playerCurent = game_manager.COMPUTER

        #Cele 4 etape MCTS
        node, matriceSimulare, playerCurent = selectie(node, matriceSimulare, playerCurent)
        node, matriceSimulare, playerCurent = expansiune(game_manager, matriceSimulare, playerCurent, node)
        matriceSimulare, playerCurent = rollout(game_manager, matriceSimulare, playerCurent)
        backpropagation(game_manager, matriceSimulare, node)

    print("\n________VERIFICARE VALORI MCTS_________")
    for move, n in root_node.children.items():
        win_rate = (n.wins / n.visits) * 100 if n.wins > 0 else 0
        print(f"Mutare {move}: Vizite: {n.visits}, Rata castig: {win_rate:.1f}%")

    # se returneaza mutarea cu cele mai multe vizitari, adica cea mai sigura
    best_move = max(root_node.children.items(), key=lambda x: x[1].visits)
    print(f"Best move: {best_move[0]}")

    return best_move[0]