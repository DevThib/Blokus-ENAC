import game as g
import math
from copy import deepcopy

def heuristique_cases(game):
    L={}
    N={}
    adversaire=0 if game.player==1 else 1
    for elem in game.piecesPlayer[game.player]:
        for version in elem.values():
            M=game.gridListener.calc_possibilities(game.player,version)
            for e in M:
                if e not in L:
                    L[e]=1
    score=len(L)
    for elem in game.piecesPlayer[adversaire]:
        for version in elem.values():
            M=game.gridListener.calc_possibilities(adversaire,version)
            for e in M:
                if e not in N:
                    N[e]=1
    score-=len(N)
    return score
                
def heuristique_pieces(game):
    score=0
    adversaire=(game.player+1)%2
    for elem in game.piecesPlayer[game.player]:
        M=[]
        for version in elem.values():
            while M==[]:
                if game.gridListener.calc_possibilities(game.player,version)!=[]:
                    M.append(1)
                    score+=1
    for elem in game.piecesPlayer[adversaire]:
        M=[]
        for version in elem.values():
            while M==[]:
                if game.gridListener.calc_possibilities(adversaire,version)!=[]:
                    M.append(1)
                    score-=1
    return score

def heuristique_bourrin(game):
    score=0
    adversaire=(game.player+1)%2
    for elem in game.piecesPlayer[game.player]:
        score-=len(elem[1])
    for elem in game.piecesPlayer[adversaire]:
        score+=len(elem[1])
    return score

def minimax(game, heuristique, player, maximisant=True, profondeur=4):
    i=0
    for elem in game.piecesPlayer[player]:
        for version in elem.values():
            if len(game.gridListener.calc_possibilities(player,version))!=0:
                i=i+1
                break
        if i!=0:
            break
    if profondeur == 0 or i == 0:
            return heuristique(game), None
    adversaire = (player+1)%2
    if maximisant:
        meilleur_score = -math.inf
        meilleur_coup = None
        for elem in game.piecesPlayer[player]:
            for version in elem.values():
                for coup in game.gridListener.calc_possibilities(player,version):
                    ng=deepcopy(game)
                    ng.gridListener.place_piece(version,coup,player)
                    score, _ = minimax(ng, heuristique, adversaire ,maximisant =False, profondeur = profondeur - 1)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
        return meilleur_score, meilleur_coup
    else:
        pire_score = math.inf
        meilleur_coup = None
        for elem in game.piecesPlayer[player]:
            for version in elem.values():
                for coup in game.gridListener.calc_possibilities(player,version):
                    ng=deepcopy(game)
                    ng.gridListener.place_piece(version,coup,player)
                    score, _ = minimax(ng, heuristique, adversaire-, maximisant =True, profondeur = profondeur - 1)
                    if score < pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
        return pire_score, meilleur_coup