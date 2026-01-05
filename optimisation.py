import game as g

def heuristique_simple(game):
    L={}
    N={}
    adversaire=0 if game.player==1 else 1
    for elem in game.piecesPlayer[game.player]:
        M=game.gridListener.calc_possibilities(game.player,elem)
        for e in M:
            if e not in L:
                L[e]=1
    score=len(L)
    for elem in game.piecesPlayer[adversaire]:
        M=game.gridListener.calc_possibilities(adversaire,elem)
        for e in M:
            if e not in N:
                N[e]=1
    score-=len(N)
    return score
                
        