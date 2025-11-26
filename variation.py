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


print(numeros(main.piece_1[1]))