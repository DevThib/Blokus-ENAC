import numpy as np
import main
import variation_2
# initialisation
plateau_joueur=[[(0,0) for i in range(24)] for j in range(24)]
for i in range(5,19):
        for j in range(0,5):
            plateau_joueur[i][j]=(2,2)
        for j in range(19,24) :
            plateau_joueur[i][j]=(2,2)
for i in range(0,5):
    for j in range(24):
        plateau_joueur[i][j]=(2,2)
for i in range(19,24):
    for j in range(24):
        plateau_joueur[i][j]=(2,2)
# premier coup la case (5,5) (resp (10,10)) doit être occupée, ici par le carré ref (i,j) de version
def coup_1(mat,version,ref) :
    for c in version :
        mat[10+ref[0]-c[0]][10-ref[1]+c[1]]=(2,2)
    for num in variation_2.numeros(version) :
        x = 10-ref[0]-num[0]
        y = 10-ref[1]+num[1]
        if y > -1 and y < len(mat) and x > -1 and x < len(mat) :
            if mat[x][y] != (2,2) :
                mat[x][y]= -num[2][0],num[2][1]
    return mat


m=coup_1(plateau_joueur,main.piece_4[2],(0,1))
for k in range(3,-3,-1) :
    print(m[10+k])
