import main
import variation_2
import matplotlib.pyplot as plt
import numpy as np
# Mise à jour de la matrice d'un joueur à partir d'une position, d'une version et d'une case de numeros(version)
def pose(mat_jeu,position,version,case) :
    f = position[0]
    g = position[1]
    o = mat_jeu[f][g]
    for c in version :
        mat_jeu[f-case[0]+c[0]][g-case[1]+c[1]]=(2,2)
    for n in variation_2.numeros(version) :
        x = f-case[0]-n[0]
        y = g-case[1]+n[1]
        if y > -1 and y < len(mat_jeu) and x > -1 and x < len(mat_jeu) :
            if mat_jeu[x][y] != (2,2) :
                mat_jeu[x][y] = n[2]
    return mat_jeu
           
mat1=[[(0,0) for i in range(6)],[(0,0),(0,0),(1,-1),(0,0),(1,1),(0,0)],[(0,0),(1,-1),(0,0),(2,2),(0,0),(0,0)],[(0,0),(0,0),(2,2),(2,2),(0,0),(0,0)],[(0,0),(-1,-1),(0,0),(0,0),(-1,1),(0,0)],[(0,0) for _ in range(6)]]
mat2=[[(0,0) for i in range(6)],[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],[(0,0),(0,0),(0,0),(2,2),(0,0),(0,0)],[(0,0),(0,0),(2,2),(2,2),(0,0),(0,0)],[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],[(0,0) for _ in range(6)]]
piece_2={1:((0,0),(0,1)),2:((0,0),(1,0))}

# Mise à jour de la matrice de jeu (0,0)=libre  (2,2) = occupé
def m_a_j(mat_jeu,position,version,case) :
    f = position[0]
    g = position[1]
    o = mat_jeu[f][g]
    for c in version :
        mat_jeu[f-case[0]+c[0]][g-case[1]+c[1]]=(2,2)
    return mat_jeu

print(pose(mat1,(4,1),((0,0),(0,1)),(0,1)))
print(m_a_j(mat2,(4,1),((0,0),(0,1)),(0,1)))
