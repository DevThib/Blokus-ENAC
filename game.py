import time

from grid import Grid
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont, QKeyEvent
import sys
import automatisation as auto
from PyQt5.QtCore import Qt
from random import randint

import optimisation as opti
import variations as v
#Ces variables permettent de modifier tous les paramètres du jeu : taille de la grille,heurisitique,profondeur...
WIDTH = 14
HEIGHT = 14
BOT_PLAY_TYPE = 2#cette variable détermine comment le bot joue (0:aléatoire,1:minimax,2:alpha_beta)
HEURISTIQUE = opti.heuristique_basique
DEPTH = 1
BOT_PLAY = True

class GameGraphics(QMainWindow):#Objet qui gère la partie interface graphique du jeu
    def __init__(self,game):
        super().__init__()
        self.game = game

        self.bot = BOT_PLAY_TYPE

        self.gridGraphics = Grid(WIDTH, HEIGHT,game)

        self.container = QWidget(objectName = "bg")
        mainHbox = QHBoxLayout()
        rightVBox = QVBoxLayout()
        piecesGrid = QGridLayout()

        self.container.setLayout(mainHbox)
        self.setWindowTitle("Blokus contre un robot")

        self.player_label = QLabel("Joueur 1")
        self.player_label.setFixedSize(500, 240) #Taille qui permet au jeu d'être affiché sur tous les ordinateurs
        self.player_label.setStyleSheet("""
                                  QLabel{
                                    color: #FFFFFF;
                                    font-family: Berlin Sans FB Demi;
                                    font-size: 120px;
                                  }
                                          """)
        self.player_label.setFont(QFont('Comic Sans MS', 60))
        self.player_label.setAlignment(Qt.AlignCenter)

        rightVBox.addWidget(self.player_label)
        rightVBox.addLayout(piecesGrid)

        i, j = 0, 0
        auto.pieces.reverse()#Mettre les plus grosses pièces en premier
        for piece in auto.pieces:
            p = GraphicPiece(piece, self.game,True)
            self.game.add_piece(p)
            piecesGrid.addWidget(p.widget, i, j)
            j += 1
            if j == 5:
                i += 1
                j = 0
        for a in range(21-len(auto.pieces)):
            p = GraphicPiece({1:[]}, self.game,False)
            piecesGrid.addWidget(p.widget, i, j)
            j += 1
            if j == 5:
                i += 1
                j = 0

        self.game.set_selected_piece(self.game.pieces[0])
        self.game.selectedPiece.bright()
        proporw = int(4 * WIDTH / 13)
        proporh = int(4 * HEIGHT / 13)
        self.gridGraphics.cases[proporh*HEIGHT+proporw].button.darken_border()

        piecesGrid.setSpacing(0)

        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)
        self.container.setStyleSheet("background-color:rgb(117,117,143);")
        self.container.setStyleSheet("""
                             QWidget#bg{
                                    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(87, 199, 133), stop:1 rgb(237, 221, 83));;
                                }
        """)
        self.container.show()
        self.setCentralWidget(self.container)
        self.setFixedSize(self.container.size())

    def update_pieces(self,player):
        for p in self.game.pieces:
            p.set_visible(p.piece in self.game.piecesPlayer[player])

    def keyPressEvent(self, event):#événement "appui d'une touche"
        if isinstance(event, QKeyEvent):
            key_text = event.text()
            if key_text == "v":
                self.game.selectedPiece.change_version(True)
            if key_text == "b":#Cette touche nous permet de faire jouer un bot contre un bot avec des configurations différentes
                if self.bot == 0:
                    self.game.bot_play(0)
                    self.bot = 2
                    return
                if self.bot == 2:
                    self.game.bot_play(2)
                    self.bot = 0
                    return



    def change_background_color(self,player):#change la couleur de fond
        if player == 0:
            self.container.setStyleSheet("""
                QWidget#bg{
                    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(87, 199, 133), stop:1 rgb(237, 221, 83));;
            }""")
        else:
            self.container.setStyleSheet("""
                QWidget#bg{
                    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 129, 0), stop:1 rgb(71, 212, 202));;
                }""")
class Game:#Objet qui gère la partie jouabilité du jeu (changement de joueur,vérification de victoire etc...)
    def __init__(self,bot):
        self.player = 0#Joueur 0:premier joueur,joueur 1:deuxième joueur
        self.pieces = []
        self.selectedPiece = None
        self.gridListener = v.GridListener(WIDTH,HEIGHT) #Objet qui gère la grille
        self.graphics = GameGraphics(self) #interface graphique
        self.piecesPlayer = ([p for p in auto.pieces],[p for p in auto.pieces])
        self.bot = bot

        self.graphics.show()

    def add_piece(self,piece):
        self.pieces.append(piece)

    def set_selected_piece(self,piece):
        self.selectedPiece = piece

    def remove_piece_for_player(self,player,piece):#retirer la pièce de la liste du joueur et de l'interface
        self.piecesPlayer[player].remove(piece)
        self.get_graphic_piece_by_piece(piece).clickable[self.player] = False

    def change_player(self):#fonction de changement de joueur,c'est elle qui actualise tout (arrière plan,texte,pièce choisie et possibilités,vérification de victoire)
        self.check_win(self.player)
        self.player = (self.player+1)%2#changement du joueur
        self.graphics.change_background_color(self.player)
        self.graphics.player_label.setText(f"Joueur {self.player+1}")#graphique
        self.graphics.update_pieces(self.player)
        if self.selectedPiece.piece not in self.piecesPlayer[self.player]:
            self.selectedPiece = self.get_graphic_piece_by_piece(self.piecesPlayer[self.player][0])#si la pièce sélectionnée précdemment n'est pas disponible,on en sélectionne une autre
        self.selectedPiece.bright()
        self.graphics.gridGraphics.clean_possibilities()
        self.gridListener.update_possibilities(self.player,self.selectedPiece.get_version())#mise à jour les cases de possibilités
        self.graphics.gridGraphics.show_possibilities(self.gridListener.possibilities[self.player])

    def get_graphic_piece_by_piece(self,piece):#récupérer une pièce graphique à partir d'un dictinnaire
        for p in self.pieces:
            if p.piece == piece:
                return p
    def place_piece(self,pos):#fonction de placement d'une pièce,c'est la fonction qui appelle et permet tout le reste (graphique,changement de joueur...)
        if pos in self.gridListener.possibilities[self.player]:
            self.gridListener.place_piece(self.selectedPiece.get_version(),pos,self.player)
            return True
        else:
            return False

    def check_win(self,player):#fonction de vérification de victoire
        if len(self.piecesPlayer[player]) == 0:print(f"Joueur {player} a gagné !!")
        impossible = True
        for piece in self.piecesPlayer[player]:
            for v in piece.values():
                if self.gridListener.has_possibilities(player, v):#dès qu'une possibilité de jeu à été trouvée,le joueur n'a pas perdu
                    impossible = False
                    break
            if not impossible:break
        if impossible and not self.gridListener.first[player]:#si aucune n'est trouvée,l'adversaire à gagné
            print(f"Joueur {(player + 1) % 2} a gagné !!")
            self.graphics.close()
            return


    def bot_play(self,type):
        if self.gridListener.first[self.player]:
            piece = self.piecesPlayer[self.player][randint(0, len(self.piecesPlayer[self.player]) - 1)]
            kk = []
            for k in piece.keys():
                kk.append(k)
            v = kk[randint(0,len(piece.keys())-1)]
            self.selectedPiece = self.get_graphic_piece_by_piece(piece)
            self.selectedPiece.version = v-1
            self.place_piece(self.gridListener.possibilities[self.player][0])
            self.graphics.gridGraphics.add_piece(piece, v, self.gridListener.possibilities[self.player][0], self.player)
            self.change_player()
            self.selectedPiece.change_version(False)
            return
        if type == 0:#Jeu aléatoire:on détermine toutes les versions jouables et on en prend une au hasard
            versions = []
            for p in self.piecesPlayer[self.player]:
                for v in p.keys():
                    if self.gridListener.has_possibilities(self.player,p[v]):versions.append((v,p))
            if len(versions) == 0:
                print(f"Joueur {(self.player + 1) % 2} a gagné !!")
                self.graphics.close()
                return
            r = randint(0,len(versions)-1)#on sélectionne une version aléatoire parmis celles jouables
            self.selectedPiece = self.get_graphic_piece_by_piece(versions[r][1])
            self.selectedPiece.version = versions[r][0]-1
            self.gridListener.update_possibilities(self.player, versions[r][1][versions[r][0]])
            poss = self.gridListener.calc_possibilities(self.player,versions[r][1][versions[r][0]])
            case = poss[randint(0,len(poss)-1)]
            self.place_piece(case)
            self.graphics.gridGraphics.add_piece(versions[r][1],versions[r][0], case,self.player)
        if type == 1:
            m = opti.minimax(self.piecesPlayer, self.gridListener, HEURISTIQUE, self.player,self.player ,True, DEPTH)
            v = 0
            for e in m[1][2].keys():
                if m[1][2][e] == m[1][1]:
                    v = e
                    break
            self.selectedPiece = self.get_graphic_piece_by_piece(m[1][2])
            self.selectedPiece.version = v-1
            self.gridListener.update_possibilities(self.player, self.selectedPiece.get_version())
            self.place_piece(m[1][0])
            self.graphics.gridGraphics.add_piece(self.selectedPiece.piece, self.selectedPiece.version + 1, m[1][0],self.player)

        if type == 2:
            m = opti.alpha_beta(self.piecesPlayer, self.gridListener, HEURISTIQUE, self.player,self.player ,True, DEPTH)
            v = 0
            for e in m[1][2].keys():
                if m[1][2][e] == m[1][1]:
                    v = e
                    break
            self.selectedPiece = self.get_graphic_piece_by_piece(m[1][2])
            self.selectedPiece.version = v-1
            self.gridListener.update_possibilities(self.player, self.selectedPiece.get_version())
            self.place_piece(m[1][0])
            self.graphics.gridGraphics.add_piece(self.selectedPiece.piece, self.selectedPiece.version + 1, m[1][0],self.player)
        self.change_player()
        self.selectedPiece.change_version(False)

class GraphicPiece:#Objet "pièce graphique",pièces bleues à droite pour choisir la pièce à jouer
    def __init__(self,piece,game,true):
        self.piece = piece#pièce représentée
        self.game = game
        self.widget = QWidget()#widget de la pièce
        self.grid = QGridLayout()#layout de la pièce
        self.version = 0
        self.versions = [t for t in piece.values()]
        self.rects = []#liste des rectangles qui la composent
        self.clickable = [true,true]#clickable pour l'un ou l'autre joueur

        for i in range(5):
            for a in range(5):
                rect = QPushButton()
                rect.setFixedSize(15, 15)
                if (i, a) in self.versions[self.version]:
                    rect.setStyleSheet("""
                        QPushButton{
                            border: 1px solid rgb(0,0,100);
                            background-color:blue;
                        }                      
                                         """)
                    self.rects.append((rect, True))
                else:
                    rect.setStyleSheet("""
                        QPushButton{
                            background-color:transparent;
                        }
                                         """)
                    self.rects.append((rect, False))

                self.grid.addWidget(rect, i, a)

        self.widget.setContentsMargins(0, 0, 0, 0)
        self.widget.mousePressEvent = lambda event: self.click()
        self.widget.setLayout(self.grid)
        self.widget.setCursor(Qt.CursorShape.PointingHandCursor)
        self.grid.setSpacing(0)

    def click(self):#fonctione qui sélectionne la pièce quand elle est cliquée
        if self.clickable[self.game.player]:
            self.game.selectedPiece = self
            self.bright()
            self.game.graphics.gridGraphics.clean_possibilities()
            self.game.gridListener.update_possibilities(self.game.player,self.game.selectedPiece.get_version())
            self.game.graphics.gridGraphics.show_possibilities(self.game.gridListener.possibilities[self.game.player])
            for p in self.game.pieces:
                if p != self and p.clickable[self.game.player]:p.dark()
    def show_possibilities(self,bot):#fonction qui affiche sur la grille les possibilités de placement
        self.game.gridListener.update_possibilities(self.game.player, self.game.selectedPiece.get_version())
        if not bot:
            try:
                for p in self.game.gridListener.possibilities[self.game.player]:
                    self.game.graphics.gridGraphics.dark_border_case(p)
            except AttributeError:pass

    def bright(self):#fonction qui met la pièce en orange
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                    QPushButton{
                        border: 1px solid rgb(225,131,0);
                        background-color:rgb(255,151,0);
                    }
                                        """)
    def dark(self):#fonction qui met la pièce en bleu
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                    QPushButton{
                        border: 1px solid rgb(0,0,100);
                        background-color:blue;
                    }
                                      """)
    def change_version(self,change):#fonction qui change la version de la pièce,appelée quand on apuie sur "v"
        if change:self.version = (self.version+1)%len(self.versions)
        for i in range(5):
            for a in range(5):
                index = 5 * i + a
                if (i, a) in self.versions[self.version]:
                    self.rects[index][0].setStyleSheet("""
                         QPushButton{
                            border: 1px solid rgb(225,131,0);
                            background-color:rgb(255,151,0);
                         }
                                                        """)
                    self.rects[index] = (self.rects[index][0],True)
                else:
                    self.rects[index][0].setStyleSheet("""
                         QPushButton{
                            background-color:transparent;
                         }
                                                        """)
                    self.rects[index] = (self.rects[index][0],False)
        self.game.graphics.gridGraphics.clean_possibilities()
        self.game.gridListener.update_possibilities(self.game.player, self.game.selectedPiece.get_version())
        self.game.graphics.gridGraphics.show_possibilities(self.game.gridListener.possibilities[self.game.player])

    def set_visible(self,visible):
        if not visible:
            for r in self.rects:
                r[0].setStyleSheet("""
                    QPushButton{
                        background-color:transparent;
                    }
                                   """)
        elif self.game.selectedPiece != self:
            self.dark()

    def get_version(self):
        return self.piece[self.version+1]

app = QApplication(sys.argv)
g = Game(BOT_PLAY)
sys.exit(app.exec_())






