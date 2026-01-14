from copy import deepcopy
from math import inf

def heuristique_cases(player,piecesPlayer,gridListener):  # nous calculons la différence de cases jouables entre le joueur et l'adversaire
    L = {}
    N = {}
    adversaire = (player+1)%2  # nous définissons l'adversaire
    for elem in piecesPlayer[player]: 
        for version in elem.values(): 
            M = gridListener.calc_possibilities(player, version)  # nous calculons les possibilités de jeu pour une version
            for e in M:
                if e not in L:
                    L[e] = 1  # nous comptons le nombre de cases où le joueur peut jouer cette version
    score = len(L)  # nous obtenons le nombre de cases jouables pour le joueur
    for elem in piecesPlayer[adversaire]:
        for version in elem.values():
            M = gridListener.calc_possibilities(adversaire, version) # même processus pour l'adversaire
            for e in M:
                if e not in N:
                    N[e] = 1
    score -= len(N)  # nous soustrayons le nombre de cases jouables de l'adversaire
    return score

def heuristique_pieces(player,piecesPlayer,gridListener):  # nous calculons la différence de pièces jouables entre le joueur et l'adversaire
    score = 0
    adversaire = (player + 1) % 2  # nous définissons l'adversaire
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if gridListener.has_possibilities(player, version):  # vrai si la version est jouable
                score += 1
                break  # nous avons trouvé une possibilité de jeu pour la pièce, pas la peine d'en chercher d'autres
    for elem in piecesPlayer[adversaire]:
        for version in elem.values():  # même processus pour l'adversaire
            if gridListener.has_possibilities(player, version):
                score -= 1
                break
    return score

def heuristique_basique(player,piecesPlayer,gridListener):  # nous faisons en sorte de jouer la plus grosse pièce possible
    score = 0

    adversaire = (player + 1) % 2  # nous définissons l'adversaire

    for elem in piecesPlayer[player]:
        score -= len(elem[1])  # nous enlevons le nombre de cases restantes dans nos pièces pas encore jouées
    for elem in piecesPlayer[adversaire]:
        score += len(elem[1])  # nous ajoutons celles de l'adversaire
    return score

def minimax(piecesPlayer,gridListener, heuristique, player, initial_player,maximisant=True, profondeur=1):  # nous voulons trouver le meilleur coup possible pour le joueur
    i = 0
    for elem in piecesPlayer[player]:
        for version in elem.values():
            if len(gridListener.calc_possibilities(player, version)) != 0:  # si nous pouvons jouer
                i = i + 1
                break
        if i != 0:
            break
    if profondeur == 0 or i == 0:  # si nous n'avons aucun coup ou que nous arrivons au bout de notre arbre de possibilités
        return heuristique(initial_player,piecesPlayer,gridListener), None  
    adversaire = (player+1)%2  # nous définissons l'adversaire
    if maximisant:  # si nous voulons maximiser
        meilleur_score = -inf  # nous initialisons le meilleur score
        meilleur_coup = None  # nous initialisons le meilleur coup
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):  # pour tous les coups possibles
                    gl = deepcopy(gridListener)  # nous copions l'état du jeu, pour ne pas le modifier en place
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)  # nous plaçons une pièce
                    pp[player].remove(elem)  # nous retirons la pièce de la liste des pièces jouables
                    score, _ = minimax(pp,gl, heuristique, adversaire, maximisant=False, profondeur=profondeur - 1,initial_player=initial_player)  # nous appelons récursivement le minimax après la pose de la pièce
                    if score > meilleur_score:  # calcul du meilleur coup possible et son score associé
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
        return meilleur_score, meilleur_coup
    else:  # nous éxécutons le même processus pour l'adversaire, en minimisant cette fois-ci
        pire_score = inf
        meilleur_coup = None
        for elem in piecesPlayer[player]:
            for version in elem.values():
                for coup in gridListener.calc_possibilities(player, version):
                    gl = deepcopy(gridListener)
                    pp = deepcopy(piecesPlayer)
                    gl.place_piece(version, coup, player)
                    pp[player].remove(elem)
                    score, _ = minimax(pp,gl, heuristique, player, maximisant=True, profondeur=profondeur - 1,initial_player=initial_player)
                    if score < pire_score:
                        pire_score = score
                        meilleur_coup = (coup,version,elem)
        return pire_score, meilleur_coup

def alpha_beta(piecesPlayer,gridListener, heuristique, player,initial_player, maximisant=True, profondeur=4,alpha=-inf,beta=inf):  # même processus que le minimax, mais plus optimisé
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
    if maximisant:  # si nous voulons maximiser
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
                    score, _ = alpha_beta(pp,gl, heuristique, adversaire,initial_player=initial_player, maximisant=False, profondeur=profondeur - 1,alpha=alpha,beta=beta)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (coup,version,elem)
                    alpha = max(alpha, score)  # alpha devient le meilleur score pour le joueur
                    if beta <= alpha:  # si le coup n'est pas optimal
                        flag = True  # nous coupons cette branche de l'arbre
                        break
                if flag:break
            if flag:break
        return meilleur_score, meilleur_coup
    else:  # même chose pour l'adversaire, mais en minimisant
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
                    score, _ = alpha_beta(pp,gl, heuristique, player,initial_player=initial_player, maximisant=True, profondeur=profondeur - 1,alpha=alpha,beta=beta)
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



