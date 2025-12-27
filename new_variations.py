import numpy as np

class GridListener:

    def __init__(self,width,height):
        self.grids = [self.init_new_grid(width+10,height+10),self.init_new_grid(width+10,height+10),self.init_new_grid(width+10,height+10)]
        self.clickable = [[],[]]
        self.first = [True,True]
        self.possibilities = [[(5,5)],[(10,10)]]
        self.width = width
        self.height = height

    def init_new_grid(self,width,height):
        grid = np.zeros((width,height))
        for i in range(height):
            for a in range(width):
                if (i < 5 or i > height-6) or (a < 5 or a > width-6):
                    grid[i,a] = 5
        return grid

    def calc_possibilities(self,player,version):
        possibilities = []
        maxs = self.get_maximums(version)
        for case in self.clickable[player]:
            for i in range(case[0]-maxs[0]-1,case[0]+maxs[0]+1):
                for a in range(case[1]-maxs[1]-1,case[1]+maxs[1]+1):
                    for c in self.corners(version,(i,a)):
                        if c in self.clickable[player]:
                            test = True
                            for t in self.get_critical_cases(version,(i,a),3)+self.adjacents((i,a),version):
                                #PROBLEME DANS LES CASES ADJACENTES
                                print(self.adjacents((i,a),version))
                                if self.grids[player][t[1],t[0]] == 5:
                                    test = False
                                    break
                            if test and (i,a) not in possibilities:
                                possibilities.append((i-5,a-5))#-5 pour qu'elle s'adapte a la grille affichée
        return possibilities

    def update_possibilities(self,player,version):
        if not self.first[player]:
            self.possibilities[player] = self.calc_possibilities(player, version)

    def ears(self,version,pos_placed):
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

    def place_piece(self,version,pos,player):
        real_pos = self.convert_pos(pos)

        if real_pos in self.clickable[player]:self.clickable[player].remove(real_pos)
        for t in version:
            self.grids[player][real_pos[1]+t[1],real_pos[0]+t[0]] = 5
            self.grids[2][real_pos[1]+t[1],real_pos[0]+t[0]] = 5
        for e in self.ears(version,real_pos):
            self.grids[player][e[0][1],e[0][0]] = e[1]
            self.clickable[player].append(e[0])
        if self.first[player]:self.first[player] = False

    def convert_pos(self,pos):
        #change la position pour l'adapater a la grille 20*20 au lieu de 14*14
        return (pos[0]+5,pos[1]+5)

    def multiplier(self,value):
        #renvoie le multiplicateur x et y:coefficient qui permet de savoir si on doit chercher en montant:descndant pour éviter les 4 disjonctions
        if value == 1:return (-1,-1)
        if value == 2: return (1, -1)
        if value == 3: return (1, 1)
        if value == 4: return (-1, 1)

    def get_maximums(self,version):
        xmax,ymax = 0,0
        for case in version:
            if case[0] > xmax:
                xmax = case[0]
            if case[1] > ymax:
                ymax = case[1]
        return (xmax,ymax)

    def get_critical_cases(self,version,pos,direction):
        #renvoie les cases critiques : la ou un emplacement doit obligatoirement être libre
        #en base x y
        cc = []
        for i in range(len(version)):
            cc.append((pos[0]+self.multiplier(direction)[0]*version[i][0],pos[1]+self.multiplier(direction)[1]*version[i][1]))
        return cc

    def neighbours(self,version,case):
        #donne le nombre de voisin d'une case (case d'une version)
        neighbours = []
        if (case[0],case[1]+1) in version:neighbours.append((case[0],case[1]+1))
        if (case[0]+1,case[1]) in version: neighbours.append((case[0]+1,case[1]))
        if (case[0]-1,case[1]) in version: neighbours.append((case[0]-1,case[1]))
        if (case[0],case[1]-1) in version: neighbours.append((case[0],case[1]-1))
        return neighbours

    def corners(self,version,case):
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
                #Si deux voisins ont même x ou meme y alors ils sont alignés et on a pas un coin
        return corners

    def adjacents(self,case,version):
        #renvoie les case adjacentes à toutes les cases d'une version
        adj = []
        for t in version:
            if (case[0]+t[0]-1,case[1]+t[1]) not in adj:adj.append((case[0]+t[0]-1,case[1]+t[1]))
            if (case[0] + t[0], case[1] + t[1]-1) not in adj:adj.append((case[0] + t[0], case[1] + t[1]-1))
            if (case[0] + t[0] + 1, case[1] + t[1]) not in adj:adj.append((case[0] + t[0] + 1, case[1] + t[1]))
            if (case[0] + t[0], case[1] + t[1]+1) not in adj:adj.append((case[0] + t[0], case[1] + t[1]+1))
        return adj
#0:vide,-1:occupée,
#1:NO,2:NE,4:SE,3:SO
#direction complémentaire en diagonale ont une somme de 5 (au final je m'e suis pas servi)


"""

#self.possibilities(0, [(0, 0), (1, 1), (0, 1), (1, 0)])
        print(self.grids[0])
        print(self.clickable[0])
        print(self.corners([(1,1),(1,0),(0,1),(2,1),(1,2)],(11,11)))
        print(self.possibilities(0,[(0,0),(1,0),(0,1),(0,2)]))
        test = self.init_new_grid(grid.width+10,grid.height+10)
        test[10,10] = 5
        for p in self.possibilities(0,[(0,0),(1,0),(0,1),(0,2),(0,3)]):
            test[p[1],p[0]] = 6
        print(test)



 for i in range(len(version)):
                #obliger d'inverser la case car elle est au format (x,y) ce qui est l'inverse du (ligne colonne)
                case_checked = (case[1]+self.multiplier(direction)[0]*version[i][1],case[0]+self.multiplier(direction)[1]*version[i][0])
                if self.grids[2][case_checked] != 0:
                    ok = False
                    print("b : check"+str(case_checked)+" case"+str(case))
                    break
                else:
                    print(case_checked[1],case_checked[0])
            if ok:possibilities.append((case[1]+self.multiplier(direction)[0]*version[-1][0],case[1]+self.multiplier(direction)[1]*version[-1][1]))
       


  def possibilities(self,player,version):
        possibilities = []
        for case in self.clickable[player]:
            print(case)
            ok = True
            direction = self.grids[player][case[1],case[0]]
            extremums = self.get_maximums(version)
            criticals = self.get_critical_cases(version,case,direction)
            for x in range(extremums[0]+1):
                for y in range(extremums[1]+1):
                    case_checked = (case[1] + self.multiplier(direction)[0] * y,case[0] + self.multiplier(direction)[1] * x)
                    if (case_checked[1],case_checked[0]) in criticals:
                        if self.grids[2][case_checked] != 0:
                            ok = False
                            break
                if not ok:break
            #remonter et à gauche = on doit placer aux extrêmes
            if ok:
                if direction == 1:
                    possibilities.append((case[0]+ self.multiplier(direction)[0] * extremums[0],case[1]+ self.multiplier(direction)[1] * extremums[1]))
                if direction == 2:
                    possibilities.append((case[0],case[1] + self.multiplier(direction)[1] * extremums[1]))
                if direction == 3:
                    possibilities.append(case)
                if direction == 4:
                    possibilities.append((case[0] + self.multiplier(direction)[0] * extremums[0],case[1]))

        return possibilities



"""