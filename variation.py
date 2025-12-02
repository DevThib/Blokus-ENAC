import main
import matplotlib.pyplot as plt
import numpy as np

def voisins(version):
    s=set()
    for e in version:
        a,b=e
        if (a,b-1) not in version:
            s.add((a,b-1))
        if (a,b+1) not in version:
            s.add((a,b+1))
        if (a-1,b) not in version:
            s.add((a-1,b))
        if (a+1,b) not in version:
            s.add((a+1,b))
        if (a-1,b-1) not in version:
            s.add((a-1,b-1))
        if (a-1,b+1) not in version:
            s.add((a-1,b+1))
        if (a+1,b-1) not in version:
            s.add((a+1,b-1))
        if (a+1,b+1) not in version:
             s.add((a+1,b+1))
    return s

def dessin(piece):
    x=[i[1] for i in piece]
    y=[i[0] for i in piece]
    fig,ax = plt.subplots()
    ax.hist2d(x,y,bins=(np.arange(-2, 7, 1), np.arange(-2, 7, 1)))
    plt.show()


def jouable(version):
    l=voisins(version)
    c=[]
    for e in l:
        a,b=e
        if (a-1,b) in version:
            c.append(e)
        elif (a+1,b) in version:
           c.append(e)
        elif (a,b-1) in version:
            c.append(e)
        elif (a,b+1) in version:
            c.append(e)
    for i in c:
        l.discard(i)
    return l


def numeros(version):
    j=jouable(version)
    c=set()
    for e in j:
        a,b=e
        if (a-1,b-1) in version:
            g=(a,b,10)
        if (a-1,b+1) in version:
            g=(a,b,11)
        if (a+1,b+1) in version:
            g=(a,b,12)
        if (a+1,b-1) in version:
            g=(a,b,13)
        c.add(g)
    return c


def decalage(version,case):
    a,b=case
    for e in version:
        c,d=e
        c=c-a
        d=d-b
        e=(c,d)




def jeu(mat,version):
    l=numeros(version)
    s=set()
    for f in range(len(mat)):
        for g in range(len(mat[0])):
            if mat[f][g]==10:
                for i in l:
                    if i[2]==12:
                        decalage(version,(i[0]+1,i[1]+1))
                        i=(f-1,g-1)
                        for k in version:
                            k=(k[0]+i[0]+1,k[1]+i[1]+1)
                            y=0
                            if mat[k[0]][k[1]] == -1:
                                y=1
                        if y==0:
                            s.add((f,g))
            elif mat[f][g]==11:
                for i in l:
                    if i[2]==13:
                        decalage(version,(i[0]+1,i[1]-1))
                        i=(f-1,g+1)
                        for k in version:
                            k=(k[0]+i[0]+1,k[1]+i[1]-1)
                            y=0
                            if mat[k[0]][k[1]] == -1:
                                y=1
                        if y==0:
                            s.add((f,g))
            elif mat[f][g]==12:
                for i in l:
                    if i[2]==10:
                        decalage(version,(i[0]-1,i[1]-1))
                        i=(f+1,g+1)
                        for k in version:
                            k=(k[0]+i[0]-1,k[1]+i[1]-1)
                            y=0
                            if mat[k[0]][k[1]] == -1:
                                y=1
                        if y==0:
                            s.add((f,g))
            elif mat[f][g]==13:
                for i in l:
                    if i[2]==11:
                        decalage(version,(i[0]-1,i[1]+1))
                        i=(f+1,g-1)
                        for k in version:
                            k=(k[0]+i[0]-1,k[1]+i[1]+1)
                            y=0
                            if mat[k[0]][k[1]] == -1:
                                y=1
                        if y==0:
                            s.add((f,g))
    return s


mat1=[[0,0,0,0,0,0],[0,0,11,-1,10,0],[0,11,-1,-1,-1,0],[0,-1,-1,-1,-1,0],[0,12,-1,-1,13,0],[0,0,0,0,0,0]]
piece_2={1:((0,0),(0,1)),2:((0,0),(1,0))}
print(jeu(mat1,piece_2[1]))
