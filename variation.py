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
            g=(a,b,10,1)
        if (a-1,b+1) in version:
            g=(a,b,11,1)
        if (a+1,b+1) in version:
            g=(a,b,12,1)
        if (a+1,b-1) in version:
            g=(a,b,13,1)
        c.add(g)
    return c
    '''elif joueur==j2:
        j=jouable(version)
        c=set()
        for e in j:
            a,b=e
            if (a-1,b-1) in version:
                g=(a,b,10,2)
            if (a-1,b+1) in version:
                g=(a,b,11,2)
            if (a+1,b+1) in version:
                g=(a,b,12,2)
            if (a+1,b-1) in version:
                g=(a,b,13,2)
            c.add(g)
        return c'''
dessin(numeros(main.piece_15[2]))

def jeu(mat,version):
    l=numeros(version)
    s=set()
    for d in mat:
        for e in d:
            if e[3]==1:
                if e[2]==10:
                    for i in l:
                        if i[2]==12:
                            # test si on peut poser la pièce
                            s.add(((i[0]+1,i[1]+1),(e[0],e[1])))
                elif e[2]==11:
                    for i in l:
                        if i[2]==13:
                            s.add(((i[0]+1,i[1]-1),(e[0],e[1])))
                elif e[2]==12:
                    for i in l:
                        if i[2]==10:
                            s.add(((i[0]-1,i[1]-1),(e[0],e[1])))
                elif e[2]==13:
                    for i in l:
                        if i[2]==11:
                            s.add(((i[0]-1,i[1]+1),(e[0],e[1])))
    return s
    

m=np.zeros((24,24),dtype='i,i,i,i')
for i in range(24):
    for j in range(24):
        m[i][j]=(i-5,j-5,0,0)

m[15][15]=(10,10,12,1)

print(jeu(m,main.piece_4[1]))
    