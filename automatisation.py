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
    v1=retournement(piece)
    D={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
    p=piece
    D[1]=piece[1]
    v=v1[1]
    D[2]=v
    for i in range(len(p[1])):
        a,b=p[1][i]
        a=b
        b=-a
        p[1][i]=(a,b)
    D[3]=p[1]
    for i in range(len(p[1])):
        a,b=p[1][i]
        a=-a
        b=-b
        p[1][i]=(a,b)
    D[4]=p[1] 
    for i in range(len(p[1])):
        a,b=p[1][i]
        a=-b
        b=a
        p[1][i]=(a,b)   
    D[5]=p[1]
    for i in range(len(v1[1])):
        a,b=v1[1][i]
        a=b
        b=-a
        v1[1][i]=(a,b)
    D[6]=v1[1]
    for i in range(len(v1[1])):
        a,b=v1[1][i]
        a=-a
        b=-b
        v1[1][i]=(a,b)
    D[7]=v1[1]
    for i in range(len(v1[1])):
        a,b=v1[1][i]
        a=-b
        b=a
        v1[1][i]=(a,b)
    D[8]=v1[1]
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