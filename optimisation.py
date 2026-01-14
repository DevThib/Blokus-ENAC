from copy import deepcopy
from math import inf
def heuristique_cases(player,piecesPlayer,gridListener):
    L = {}
    N = {}
    adversaire = 0 if player == 1 else 1
    for elem in piecesPlayer[player]:
        for version in elem.values():
            M = gridListener.calc_possibilities(player, version)
            for e in M:
                if e not in L:
                    L[e] = 1
    score = len(L)
    for elem in piecesPlayer[adversaire]:
        for version in elem.values():
            M = gridListener.calc_possibilities(adversaire, version)
            for e in M:
                if e not in N:
                    N[e] = 1
    score -= len(N)
    return score


def heuristique_pieces(player,piecesPlayer,gridListener):
    score = 0
    adversaire = (player + 1) % 2
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if gridListener.has_possibilities(player, version):
                score += 1
                break
    for elem in piecesPlayer[adversaire]:
        for version in elem.values():
            if gridListener.has_possibilities(player, version):
                score -= 1
                break
    return score


def heuristique_bourrin(player,piecesPlayer,gridListener):
    score = 0

    adversaire = (player + 1) % 2

    for elem in piecesPlayer[player]:
        score -= len(elem[1])
    for elem in piecesPlayer[adversaire]:
        score += len(elem[1])
    return score
def minimax(piecesPlayer,gridListener, heuristique, player, maximisant=True, profondeur=4):
    i=0
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if len(gridListener.calc_possibilities(player,version))!=0:
                i=i+1
                break
        if i!=0:
            break
    if profondeur == 0 or i == 0:
        return heuristique(player,piecesPlayer,gridListener), None
    adversaire = (player+1)%2
    if maximisant:
        meilleur_score = inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player,version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = minimax(pp,gl, heuristique, adversaire ,maximisant =False, profondeur = profondeur - 1)
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
        return meilleur_score, meilleur_coup
    else:
        pire_score = -inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player,version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = minimax(pp,gl, heuristique, adversaire, maximisant =True, profondeur = profondeur - 1)
                    if score > pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
        return pire_score, meilleur_coup

def alpha_beta(piecesPlayer,gridListener, heuristique, player, maximisant=True, profondeur=4,alpha = -inf,beta = inf):
    i=0
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if len(gridListener.calc_possibilities(player,version))!=0:
                i=i+1
                break
        if i!=0:
            break
    if profondeur == 0 or i == 0:
        return heuristique(player,piecesPlayer,gridListener), None
    adversaire = (player+1)%2
    if maximisant:
        meilleur_score = inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player,version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = alpha_beta(pp,gl, heuristique, adversaire ,maximisant =False, profondeur = profondeur - 1,alpha = alpha,beta = beta)
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return meilleur_score, meilleur_coup
    else:
        pire_score = -inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player,version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = alpha_beta(pp,gl, heuristique, adversaire, maximisant =True, profondeur = profondeur - 1,alpha = alpha,beta = beta)
                    if score > pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break

        return pire_score, meilleur_coup

def minimax_2(piecesPlayer,gridListener, heuristique, player, initial_player,maximisant=True, profondeur=4):
    i = 0
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if len(gridListener.calc_possibilities(player, version)) != 0:
                i = i + 1
                break
        if i != 0:
            break
    if profondeur == 0 or i == 0:
        return heuristique(initial_player,piecesPlayer,gridListener), None
    adversaire = (player+1)%2
    if maximisant:
        meilleur_score = -inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = minimax_2(pp,gl, heuristique, adversaire, maximisant=False, profondeur=profondeur - 1,initial_player=initial_player)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
        return meilleur_score, meilleur_coup
    else:
        pire_score = inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = minimax_2(pp,gl, heuristique, player, maximisant=True, profondeur=profondeur - 1,initial_player=initial_player)
                    if score < pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
        return pire_score, meilleur_coup

def alpha_beta_2(piecesPlayer,gridListener, heuristique, player,initial_player, maximisant=True, profondeur=4,alpha=-inf,beta=inf):
    i = 0
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if len(gridListener.calc_possibilities(player, version)) != 0:
                i = i + 1
                break
        if i != 0:
            break
    if profondeur == 0 or i == 0:
        return heuristique(initial_player,piecesPlayer,gridListener), None
    adversaire = (player+1)%2
    if maximisant:
        meilleur_score = -inf
        meilleur_coup = None
        flag = False
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = alpha_beta_2(pp,gl, heuristique, adversaire,initial_player=initial_player, maximisant=False, profondeur=profondeur - 1,alpha=alpha,beta=beta)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        flag = True
                        break
                if flag:break
            if flag:break
        return meilleur_score, meilleur_coup
    else:
        pire_score = inf
        meilleur_coup = None
        flag = False
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = alpha_beta_2(pp,gl, heuristique, player,initial_player=initial_player, maximisant=True, profondeur=profondeur - 1,alpha=alpha,beta=beta)
                    if score < pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
                    beta = min(beta, score)
                    if beta <= alpha:
                        flag = True
                        break
                if flag:break
            if flag:break
        return pire_score, meilleur_coup

"""class MinimaxTester:
    def __init__(self,grids):
        self.grids = grids
        
    def test(self,player,c):"""

