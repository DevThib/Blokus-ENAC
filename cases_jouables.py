#import main
import matplotlib.pyplot as plt
import numpy as np
# Crée le contour de la pièce
def voisins(version):
    s=set()
    for e in version:
        a,b=e
        for i in range(-1,2) :
            for j in range(-1,2):
                if (a+i,b+j) not in version :
                    s.add((a+i,b+j))
    return s
# Outil de représentation visuelle
def dessin(piece):
    x=[i[1] for i in piece]
    y=[i[0] for i in piece]
    fig,ax = plt.subplots()
    ax.hist2d(x,y,bins=(np.arange(-2, 7, 1), np.arange(-2, 7, 1)))
    plt.show()

# Enlève de l'enveloppe les éléments ayant une arète commune avec la piece
def jouable(version):
    l=voisins(version)
    c=[]
    for e in l:
        a,b=e
        if (a-1,b) in version or (a+1,b) in version or (a,b-1) in version or (a,b+1) in version:
            c.append(e)
    for i in c:
        l.discard(i)
    return l

# Attribue une orientation aux éléments d'angle de la pièce
def numeros(version):
    j=jouable(version)
    c=set()
    for e in j:
        a,b=e
        # NE = (1,1)
        if (a-1,b-1) in version:
            g=(a,b,(1,1))
        # NW = (1,-1)
        if (a-1,b+1) in version:
            g=(a,b,(1,-1))
        # SW = (-1,-1)
        if (a+1,b+1) in version:
            g=(a,b,(-1,-1))
        # SE = (-1,1)
        if (a+1,b-1) in version:
            g=(a,b,(-1,1))
        c.add(g)
    return c

# Redéfinie les coordonnées locales de la pièce par rapport à la case (a,b) qui devient (0,0)
def decalage(version,case):
    a,b=case
    for e in version:
        c,d=e
        c=c-a
        d=d-b
        e=(c,d)
    return version

# La matrice de jeu a comme chaque élément un tuple soit (0,0)=vide, soit orientation=vide_et_jouable, soit (2,2)=occupé
# La fonction fournit un dictionnaire de cases jouables de la matrice avec comme clé l'orientation
def jeu(mat,version):
    l1=voisins(version)
    #print(l1)
    l2=jouable(version)
    #print(l2)
    l=numeros(version)
    #print(l)
    orientation=((1,1),(1,-1),(-1,-1),(-1,1))
    cases_jouables={o:set() for o in orientation}
    for f in range(len(mat)):
        for g in range(len(mat[0])):
            for o in orientation :
                o_x=o[0]
                o_y=o[1]
                if mat[f][g]==o:
                    for i in l:
                        if i[2]==(-o_x,-o_y):
                            for k in decalage(version,(i[0]-o_x,i[1]-o_y)) :
                                k=(k[0]+f,k[1]+g)
                                y=0
                                if k[0]<0 or k[0]>len(mat)-1 :
                                    y=1
                                elif k[1]<0 or k[1]>len(mat)-1:
                                    y=1
                                elif mat[k[0]][k[1]] == (2,2):
                                    y=1
                            if y==0:
                                cases_jouables[o].add((f,g))
    return cases_jouables


mat1=[[(0,0) for i in range(6)],[(0,0),(0,0),(1,-1),(2,2),(1,1),(0,0)],[(0,0),(1,-1),(2,2),(2,2),(2,2),(0,0)],[(0,0),(2,2),(2,2),(2,2),(2,2),(0,0)],[(0,0),(-1,-1),(2,2),(2,2),(-1,1),(0,0)],[(0,0) for _ in range(6)]]
piece_2={1:((0,0),(0,1)),2:((0,0),(1,0))}
print(jeu(mat1,piece_2[2]))