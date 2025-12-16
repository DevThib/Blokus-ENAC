import bibliotheque_pieces as bb

def retournement(piece):
    retournement={1:[]}
    L=[]
    M=[]
    amax=0
    bmax=0
    for i in range(len(piece[1])):
        if piece[1][i][0]>amax:
            amax=piece[1][i][0]
        if piece[1][i][1]>bmax:
            bmax=piece[1][i][1]
    moy_a=amax/2
    moy_b=bmax/2
    for i in range(len(piece[1])):
        L.append((piece[1][i][0]-moy_a,piece[1][i][1]-moy_b))
        M.append((int(-L[i][0]+moy_a),int(L[i][1]+moy_b)))
    retournement[1]=sorted(M)
    return retournement

def rotation(piece):
    rotation={1:[]}
    L=[]
    M=[]
    amax=0
    bmax=0
    for i in range(len(piece[1])):
        if piece[1][i][0]>amax:
            amax=piece[1][i][0]
        if piece[1][i][1]>bmax:
            bmax=piece[1][i][1]
    moy_a=amax/2
    moy_b=bmax/2
    for i in range(len(piece[1])):
        L.append((piece[1][i][0]-moy_a,piece[1][i][1]-moy_b))
        M.append((int(L[i][1]+moy_b),int(-L[i][0]+moy_a)))
    rotation[1]=sorted(M)
    return rotation


def versions(piece):
    r1=rotation(piece)
    piece[2]=r1[1]     
    r2=rotation(r1)
    piece[3]=r2[1]
    r3=rotation(r2)
    piece[4]=r3[1]
    ret=retournement(piece)
    piece[5]=ret[1]
    r11=rotation(ret)
    piece[6]=r11[1]
    r12=rotation(r11)
    piece[7]=r12[1]
    r13=rotation(r12)
    piece[8]=r13[1]
    for i in range(1,9):
        for j in range(i+1,9):
            if piece[i]==piece[j]:
                piece[j]=[]
    for k in range(1,9):
        if piece[k]==[]:
            del piece[k]
    return piece

pieces=[versions(bb.piece_1),versions(bb.piece_2),versions(bb.piece_3),versions(bb.piece_4),versions(bb.piece_5),versions(bb.piece_6),versions(bb.piece_7),versions(bb.piece_8),versions(bb.piece_9),versions(bb.piece_10),versions(bb.piece_11),versions(bb.piece_12),versions(bb.piece_13),versions(bb.piece_14),versions(bb.piece_15),versions(bb.piece_16),versions(bb.piece_17),versions(bb.piece_18),versions(bb.piece_19),versions(bb.piece_20),versions(bb.piece_21)]
print(pieces)
