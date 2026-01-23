import pieces_library as bb

def retournement(piece):
    retournement={1:[]}
    L=[]
    M=[]
    amax=0
    bmax=0
    for i in range(len(piece[1])):
        if piece[1][i][0]>amax:
            amax=piece[1][i][0]  # on calcule la taille de la pièce
        if piece[1][i][1]>bmax:
            bmax=piece[1][i][1]
    moy_a=amax/2   # on place l'origine du repère de la pièce au centre géométrique
    moy_b=bmax/2   
    for i in range(len(piece[1])):
        L.append((piece[1][i][0]-moy_a,piece[1][i][1]-moy_b))  # on applique le retournement
        M.append((int(-L[i][0]+moy_a),int(L[i][1]+moy_b)))  # on remet en haut à gauche l'origine de la pièce
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
            amax=piece[1][i][0]  # on calcule la taille de la pièce
        if piece[1][i][1]>bmax:
            bmax=piece[1][i][1]
    moy_a=amax/2  # on place l'origine du repère de la pièce au centre géométrique
    moy_b=bmax/2
    for i in range(len(piece[1])):
        L.append((piece[1][i][0]-moy_a,piece[1][i][1]-moy_b))  # on applique la rotation
        M.append((int(L[i][1]+moy_b),int(-L[i][0]+moy_a)))  # on remet en haut à gauche l'origine de la pièce
    rotation[1]=sorted(M)
    return rotation


def versions(piece):
    r1=rotation(piece)  # on calcule chaque version et on les ajoute au dictionnaire de la pièce
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
    for i in range(1,9):  # on supprime les doublons
        for j in range(i+1,9):
            if piece[i]==piece[j]:
                piece[j]=[]
    for k in range(1,9):
        if piece[k]==[]:
            del piece[k]
    new_piece = {}#réaffectation des clés pour palier à une erreur d'affectation
    i = 1
    for k in piece.keys():
        new_piece[i] = piece[k]
        i += 1
    return new_piece

pieces=[versions(bb.piece_1),versions(bb.piece_2),versions(bb.piece_3),versions(bb.piece_4),versions(bb.piece_5),versions(bb.piece_6),versions(bb.piece_7),versions(bb.piece_8),versions(bb.piece_9),versions(bb.piece_10),versions(bb.piece_11),versions(bb.piece_12),versions(bb.piece_13),versions(bb.piece_14),versions(bb.piece_15),versions(bb.piece_16),versions(bb.piece_17),versions(bb.piece_18),versions(bb.piece_19),versions(bb.piece_20),versions(bb.piece_21)]

