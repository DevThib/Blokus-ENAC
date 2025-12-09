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
    n=len(piece)
    v1=retournement(piece)
    D={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    D[1]=piece[1].copy()
    D[2]=v1[1].copy()
    for i in range(n):
        a,b=piece[1][i]
        a=b
        b=-a
        D[3].append(a,b)
    for i in range(len(piece[1])):
        p2=piece.copy()
        a,b=p2[1][i]
        a=-a
        b=-b
        p2[1][i]=(a,b)
    D[4]=p2[1]
    for i in range(len(piece[1])):
        p3=piece.copy()
        a,b=p3[1][i]
        a=-b
        b=a
        p3[1][i]=(a,b)   
    D[5]=p3[1]
    for i in range(len(v1[1])):
        p4=v1.copy()
        a,b=p4[1][i]
        a=b
        b=-a
        p4[1][i]=(a,b)
    D[6]=p4[1]
    for i in range(len(v1[1])):
        p5=v1.copy()
        a,b=p5[1][i]
        a=-a
        b=-b
        p5[1][i]=(a,b)
    D[7]=p5[1]
    for i in range(len(v1[1])):
        p6=v1.copy()
        a,b=p6[1][i]
        a=-b
        b=a
        p6[1][i]=(a,b)
    D[8]=p6[1]
    for i in range(1,8):
        for j in range(i+1,9):
            if D[i]==D[j]:
                D[j]=[]
    for k in range(1,9):
        if D[k]==[]:
            del D[k]
    return D   
        
piece_2={1:[(0,0),(0,1)]}
print(versions(piece_2))