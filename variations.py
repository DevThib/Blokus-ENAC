import numpy as np

class GridListener:#objet qui gère tous les calculs relatifs à la grille

    def __init__(self,width,height):
        self.grids = [self.init_new_grid(width+10,height+10),self.init_new_grid(width+10,height+10),self.init_new_grid(width+10,height+10)]#trois grilles : deux pour les joueurs qui contiennent les cases occupées par le joueur et d'autres donnnées
                                                                                                                                           # et une "globale" qui ne contient que des 0 et 5 et représente les cases occupées sans distinction de joueur
        self.clickable = [[],[]]
        self.first = [True,True]
        self.possibilities = [[(4,4)],[(9,9)]]
        self.width = width
        self.height = height

    def init_new_grid(self,width,height):#création de la matrice en (width+5)*(height+5)
        grid = np.zeros((width,height))
        for i in range(height):
            for a in range(width):
                if (i < 5 or i > height-6) or (a < 5 or a > width-6):
                    grid[i,a] = 5#les cases de 0 à 4 et de width à width+4,height à height+4 sont déjà prises,une grille plus grande permet de s'affranchir d'éventuels "IndexError"
        return grid

    def calc_possibilities(self,player,version):#fonction de calcul des possibilités
        possibilities = []
        maxs = self.get_maximums(version)
        checked = []
        for case in self.clickable[player]:
            for i in range(case[0]-maxs[0]-1,case[0]+maxs[0]+1):#on parcourt les rectangles des dimensions de la pièce,ce sont les seuls endroits ou il peut y avoir des possibilités (voir get_maximums)
                for a in range(case[1]-maxs[1]-1,case[1]+maxs[1]+1):
                    if(i,a) not in checked:
                        for c in self.corners(version,(i,a)):#les coins sont les cases la pièce qui concordent avec les oreilles,on ne regarde donc qu'eux
                            if c in self.clickable[player]:
                                test = True#si ce booléen reste vrai notre case est une possibilité de jeu
                                for t in self.get_critical_cases(version,(i,a),3):
                                    if self.grids[2][t[1],t[0]] == 5.0: #cases critiques = obligatoirement libres
                                        test = False
                                        break
                                for t in self.adjacents((i,a),version):
                                    if t[1] >= 5 and t[1] <= 18 and t[0] >= 5 and t[0] <= 18:
                                        if self.grids[player][t[1], t[0]] == 5.0:#cases adjacentes = il ne faut pas que ce soit une case du joueur (jeu en diagonale)
                                            test = False
                                            break
                                if test and (i,a) not in possibilities:
                                    possibilities.append((i-5,a-5))#-5 pour qu'elle s'adapte a la grille affichée
                                checked.append((i,a))
        return possibilities

    def has_possibilities(self,player,version):#renvoie un booléen : "y'a t-il une possibilité ? de jouer cette version",elle s'arrête dès qu'elle en a trouvé une
        possibility = False
        maxs = self.get_maximums(version)
        checked = []
        for case in self.clickable[player]:
            for i in range(case[0] - maxs[0] - 1, case[0] + maxs[0] + 1):
                for a in range(case[1] - maxs[1] - 1, case[1] + maxs[1] + 1):
                    if (i, a) not in checked:
                        for c in self.corners(version, (i, a)):
                            if c in self.clickable[player]:
                                test = True
                                for t in self.get_critical_cases(version, (i, a), 3):
                                    if self.grids[2][t[1], t[0]] == 5.0:  # cases critiques = obligatoirement libres
                                        test = False
                                        break
                                for t in self.adjacents((i, a), version):
                                    if t[1] >= 5 and t[1] <= 18 and t[0] >= 5 and t[0] <= 18:
                                        if self.grids[player][t[1], t[0]] == 5.0:  # cases adjacentes = il ne faut pas que ce soit une case du joueur
                                            test = False
                                            break
                                if test:
                                    possibility = True
                                    break
                        if possibility: break
                if possibility: break#CA PLANTE
            if possibility: break
        return possibility
    def update_possibilities(self,player,version):#mise à jour des possibilités
        if not self.first[player]:
            self.possibilities[player] = self.calc_possibilities(player, version)

    def ears(self,version,pos_placed):#fonction de calcul des "oreilles" d'une version: cases en diagonale de la pièce
        ears = []
        for t in version:
            if (t[0]-1,t[1]) not in version and (t[0],t[1]-1) not in version:
                ears.append(((pos_placed[0]+t[0]-1,pos_placed[1]+t[1]-1),1))
            if (t[0]+1,t[1]) not in version and (t[0],t[1]-1) not in version:
                ears.append(((pos_placed[0]+t[0]+1,pos_placed[1]+t[1]-1),3))
            if (t[0]+1,t[1]) not in version and (t[0],t[1]+1) not in version:
                ears.append(((pos_placed[0]+t[0]+1,pos_placed[1]+t[1]+1),4))
            if (t[0]-1,t[1]) not in version and (t[0],t[1]+1) not in version:
                ears.append(((pos_placed[0]+t[0]-1,pos_placed[1]+t[1]+1),2))
        return ears

    def place_piece(self,version,pos,player):#fonction qui place une pièce dans la matrice
        real_pos = self.convert_pos(pos)

        if real_pos in self.clickable[player]:self.clickable[player].remove(real_pos)
        for t in version:
            self.grids[player][real_pos[1]+t[1],real_pos[0]+t[0]] = 5#les cases prises deviennent des 5
            self.grids[2][real_pos[1]+t[1],real_pos[0]+t[0]] = 5
        for e in self.ears(version,real_pos):#on met à jour les oreilles des cases dans la matrice
            if self.grids[player][e[0][1],e[0][0]] != 5.0:
                self.grids[player][e[0][1],e[0][0]] = e[1]
                self.clickable[player].append(e[0])
        if self.first[player]:self.first[player] = False

    def convert_pos(self,pos):#change la position pour l'adapater a la grille 20*20 au lieu de 14*14
        return (pos[0]+5,pos[1]+5)

    def multiplier(self,value):#renvoie le multiplicateur x et y:coefficient qui permet de savoir si on doit chercher en montant:descndant pour éviter les 4 disjonctions
        if value == 1:return (-1,-1)
        if value == 2: return (1, -1)
        if value == 3: return (1, 1)
        if value == 4: return (-1, 1)

    def get_maximums(self,version):#donne la "taille" d'une pièce (x et y maximaux dans la liste de tuples),ex: la pièce + est une pièce 3*3
        xmax,ymax = 0,0
        for case in version:
            if case[0] > xmax:
                xmax = case[0]
            if case[1] > ymax:
                ymax = case[1]
        return (xmax,ymax)

    def get_critical_cases(self,version,pos,direction):
        #renvoie les "cases critiques" : cases pour lesquelles un emplacement doit obligatoirement être libre car ce seront les cases occupées quand la pièce sera posée
        #en base x y
        cc = []
        for i in range(len(version)):
            cc.append((pos[0]+self.multiplier(direction)[0]*version[i][0],pos[1]+self.multiplier(direction)[1]*version[i][1]))
        return cc

    def neighbours(self,version,case):#donne le nombre de voisin d'une case (case d'une version)
        neighbours = []
        if (case[0],case[1]+1) in version:neighbours.append((case[0],case[1]+1))
        if (case[0]+1,case[1]) in version: neighbours.append((case[0]+1,case[1]))
        if (case[0]-1,case[1]) in version: neighbours.append((case[0]-1,case[1]))
        if (case[0],case[1]-1) in version: neighbours.append((case[0],case[1]-1))
        return neighbours

    def corners(self,version,case):#renvoie les coins d'une pièce et ses extrémité
        corners = []
        for c in version:
            n = self.neighbours(version,c)
            if len(n) <= 1:
                corners.append((case[0]+c[0],case[1]+c[1]))
            else:
                for nei in n:
                    test = False
                    for other in n:
                        if nei != other and (nei[0] == other[0] or nei[1] == other[1]):
                            test = True
                    if not test:
                        corners.append((case[0] + c[0], case[1] + c[1]))
                #Si deux voisins ont même x ou meme y alors ils sont alignés et ce n'est pas un coin
        return corners

    def adjacents(self,case,version):#renvoie les case adjacentes à toutes les cases d'une version
        adj = []
        for t in version:
            if (case[0]+t[0]-1,case[1]+t[1]) not in adj:adj.append((case[0]+t[0]-1,case[1]+t[1]))
            if (case[0] + t[0], case[1] + t[1]-1) not in adj:adj.append((case[0] + t[0], case[1] + t[1]-1))
            if (case[0] + t[0] + 1, case[1] + t[1]) not in adj:adj.append((case[0] + t[0] + 1, case[1] + t[1]))
            if (case[0] + t[0], case[1] + t[1]+1) not in adj:adj.append((case[0] + t[0], case[1] + t[1]+1))
        return adj

#0:vide,5:occupée,
#1:NO,2:NE,4:SE,3:SO

