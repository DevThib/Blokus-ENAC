import game as g

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