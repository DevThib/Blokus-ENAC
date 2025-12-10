def retournement(piece):
    retourne={1:[]}
    L=[]
    for i in range(len(piece[1])):
        a,b=piece[1][i]
        a=-a
        L.append((a,b))
    retourne[1]=L
    return retourne


def versions(piece):
    n=len(piece[1])
    v1=retournement(piece)
    D={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    D[1]=piece[1].copy()
    D[1]=sorted(D[1])
    for i in range(n):
        a,b=piece[1][i]
        afin=b
        b=-a
        D[2].append((afin,b))
    D[2]=sorted(D[2])
    for i in range(n):
        a,b=piece[1][i]
        afin=-a
        b=-b
        D[3].append((afin,b))
    D[3]=sorted(D[3])
    for i in range(n):
        a,b=piece[1][i]
        afin=-b
        b=a
        D[4].append((afin,b))
    D[4]=sorted(D[4])
    D[5]=v1[1]
    D[5]=sorted(D[5])
    for i in range(n):
        a,b=v1[1][i]
        afin=b
        b=-a
        D[6].append((afin,b))
    D[6]=sorted(D[6])
    for i in range(n):
        a,b=v1[1][i]
        afin=-a
        b=-b
        D[7].append((afin,b))
    D[7]=sorted(D[7])
    for i in range(n):
        a,b=v1[1][i]
        afin=-b
        b=a
        D[8].append((afin,b))
    D[8]=sorted(D[8])
    for i in range(1,8):
        for j in range(i+1,9):
            if D[i]==D[j]:
                D[j]=[]
    for k in range(1,9):
        if D[k]==[]:
            del D[k]
    return D   
        
piece_17={1:[(0,0),(0,1),(0,2),(1,0),(2,0)]}
print(versions(piece_17))


