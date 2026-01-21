from PyQt5.QtWidgets import  QWidget, QPushButton,QGridLayout
from PyQt5.QtCore import Qt

class Grid:

    def __init__(self, width, height,game):
        self.width = width
        self.height = height
        self.cases = []
        self.grid = self.build_grid()
        self.game = game

    def build_grid(self):#construction de la grille graphique
        container = QWidget()
        gridLayout = QGridLayout()
        container.setLayout(gridLayout)

        gridLayout.setSpacing(0)

        for i in range(self.height):
            for a in range(self.width):
                c = Case(i,a,self)
                gridLayout.addWidget(c.button,i,a)
                self.cases.append(c)
        return container
    def add_piece(self, piece,version, pos,player):#ajout dune pièce sur la gille
        for t in piece[version]:
            if pos[0]+t[0] < self.width and pos[1]+t[1]< self.height:
                case = self.cases[(pos[0] + t[0]) * self.height + (pos[1] + t[1])]
                case.change_color(player)
                case.clickable = False
        self.game.remove_piece_for_player(player, piece)
    def dark_border_case(self,pos):#surlignage de la case en noir (affichage des possibilités de jeu)
        self.cases[pos[0]*self.width+pos[1]].button.darken_border()
    def grey_border_case(self,pos):#remettre la bordure de la case en gris
        self.cases[pos[0]*self.width+pos[1]].button.greyen_border()

    def clean_possibilities(self):#retirer toutes les cases en surlignage noir
        for c in self.cases:
            if c.clickable:
                c.button.greyen_border()
    def show_possibilities(self,possibilities_list):#affichage des possibilités de jeu
        for c in possibilities_list:
            self.cases[c[0]*self.height+c[1]].button.darken_border()

class Case:
    def __init__(self,x,y,grid):
        self.grid = grid
        self.button = self.create_button()
        self.x = x
        self.y = y
        self.clickable = True

    def create_button(self):
        class CaseButton(QPushButton):#Le bouton est un objet créé par nous même car il doit hériter de QPushbutton pour avoir les évènements d'entrée et de sortie de la souris
            def __init__(self,case):
                super().__init__()
                self.clicked.connect(case.on_clicked)
                GRID_SIZE = 700#700 pixels:taille de la grille
                self.setFixedSize(int(GRID_SIZE/case.grid.width), int(GRID_SIZE/case.grid.height))
                self.setCursor(Qt.CursorShape.PointingHandCursor)
                self.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(150,150,150);
                        border:2.5px solid rgb(100,100,100);
                    }                                    
                                    """)

                self.case = case
            def enterEvent(self, a0):#lorsque la souris entre,nous surlignons en orange les cases correspondant à la pièce (prévisualisation d'un éventuel placement)
                pos = (self.case.x,self.case.y)
                for c in self.case.grid.game.selectedPiece.get_version():
                    if (pos[0]+c[0])*self.case.grid.width+pos[1]+c[1] < self.case.grid.height*self.case.grid.width:
                        cb = self.case.grid.cases[(pos[0]+c[0])*self.case.grid.width+pos[1]+c[1]]
                        if cb.clickable:
                            cb.button.setStyleSheet("""
                                QPushButton {
                                    background-color: rgb(150,150,150);
                                    border:2.5px solid orange;
                                }                           
                                                    """)
            def leaveEvent(self, a0):#lorsque la souris sort,nous retirons ce surlignage en orange
                pos = (self.case.x,self.case.y)
                for c in self.case.grid.game.selectedPiece.get_version():
                    if (pos[0]+c[0])*self.case.grid.width+pos[1]+c[1] < self.case.grid.height*self.case.grid.width:
                        cb = self.case.grid.cases[(pos[0] + c[0]) * self.case.grid.width + pos[1] + c[1]]
                        if (pos[0] + c[0], c[1] + pos[1]) in self.case.grid.game.gridListener.possibilities[self.case.grid.game.player]:
                            cb.button.darken_border()
                        else:
                            cb.button.greyen_border()
            def darken_border(self):#mise de la bordure en noir
                if self.case.clickable:
                    self.setStyleSheet("""
                        QPushButton {
                            background-color: rgb(150,150,150);
                            border:2.5px solid black;
                        }
                                    """)

            def greyen_border(self):#mise de la bourdure en gris
                if self.case.clickable:
                    self.setStyleSheet("""
                        QPushButton {
                            background-color: rgb(150,150,150);
                            border:2.5px solid rgb(100,100,100);
                        }
                                """)

        return CaseButton(self)

    def on_clicked(self):#fonction éxécutée quand on clique sur une case
        if self.grid.game.place_piece((self.x, self.y)):#si jeu possible alors on ajoute la pièce à la grille et on change de joueur
            self.grid.add_piece(self.grid.game.selectedPiece.piece, self.grid.game.selectedPiece.version + 1,(self.x, self.y), self.grid.game.player)
            self.grid.game.change_player()
            if self.grid.game.bot:
                self.grid.game.bot_play(self.grid.game.graphics.bot)
    def change_color(self,player):#fonction qui met la case en vert ou rouge quand un joueur a joué
        if player == 0:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid rgb(0,90,0);
                    background-color:rgb(0,140,0);
                }
                                     """)
        else:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                QPushButton {
                    border: 1px solid rgb(90,0,0);
                    background-color:rgb(140,0,0);
                }
                                     """)