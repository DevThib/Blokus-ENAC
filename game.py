from grid import Grid
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont, QKeyEvent
import sys
import automatisation as auto
from PyQt5.QtCore import Qt
from random import randint

import optimisation as opti
import variations as v

class GameGraphics(QMainWindow):#Objet qui gère la partie graphique du jeu
    def __init__(self,game):
        super().__init__()
        self.game = game

        self.gridGraphics = Grid(14, 14,game)

        self.container = QWidget(objectName = "bg")
        mainHbox = QHBoxLayout()
        rightVBox = QVBoxLayout()
        piecesGrid = QGridLayout()

        self.container.setLayout(mainHbox)
        self.setWindowTitle("Blokus contre un robot")

        self.player_label = QLabel("Joueur 1")
        self.player_label.setFixedSize(500, 240)
        self.player_label.setStyleSheet("""
                                  QLabel{
                                    color: #FFFFFF;
                                    font-family: Goudy stout;
                                    font-size: 50px;
                                  }
                                          """)
        self.player_label.setFont(QFont('Comic Sans MS', 60))
        self.player_label.setAlignment(Qt.AlignCenter)

        rightVBox.addWidget(self.player_label)
        rightVBox.addLayout(piecesGrid)

        i, j = 0, 0
        for piece in auto.pieces:
            p = GraphicPiece(piece, self.game)
            self.game.add_piece(p)
            piecesGrid.addWidget(p.widget, i, j)
            j += 1
            if j == 5:
                i += 1
                j = 0
        self.game.set_selected_piece(self.game.pieces[0])
        self.game.selectedPiece.bright()
        self.gridGraphics.cases[4*14+4].button.darken_border()

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
                self.game.selectedPiece.change_version()

    def change_background_color(self,player):
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
        self.player = 0
        self.pieces = []
        self.selectedPiece = None
        self.gridListener = v.GridListener(14,14)
        self.graphics = GameGraphics(self)
        self.piecesPlayer = ([p for p in auto.pieces],[p for p in auto.pieces])
        self.bot = bot

        self.graphics.show()

    def add_piece(self,piece):
        self.pieces.append(piece)

    def set_selected_piece(self,piece):
        self.selectedPiece = piece

    def remove_piece_for_player(self,player,piece):
        self.piecesPlayer[player].remove(piece)
        self.get_graphic_piece_by_piece(piece).clickable[self.player] = False

    def change_player(self):
        self.player = (self.player+1)%2
        self.graphics.change_background_color(self.player)
        self.graphics.player_label.setText(f"Joueur {self.player+1}")
        self.graphics.update_pieces(self.player)
        if self.selectedPiece.piece not in self.piecesPlayer[self.player]:
            self.selectedPiece = self.get_graphic_piece_by_piece(self.piecesPlayer[self.player][0])
        self.selectedPiece.bright()
        self.graphics.gridGraphics.clean_possibilities()
        self.gridListener.update_possibilities(self.player,self.selectedPiece.get_version())
        self.graphics.gridGraphics.show_possibilities(self.gridListener.possibilities[self.player])
        self.check_win((self.player+1)%2)

    def get_graphic_piece_by_piece(self,piece):
        for p in self.pieces:
            if p.piece == piece:
                return p
    def place_piece(self,pos):
        if pos in self.gridListener.possibilities[self.player]:
            self.gridListener.place_piece(self.selectedPiece.get_version(),pos,self.player)
            return True
        else:
            return False

    def check_win(self,player):
        if 21-len(self.piecesPlayer[player]) > 5:#on ne cherche pas a vérifier avant le 5ème tour ca sert a rien
            imp = 0
            for piece in self.piecesPlayer[player]:
                impossible = True
                for v in piece.keys():
                    poss = self.gridListener.calc_possibilities(player, piece[v])
                    if len(poss) != 0:
                        impossible = False
                if impossible:imp += 1
            if imp == len(self.piecesPlayer[player]):
                print(f"Joueur {(player + 1) % 2} à gagné !!")
                self.graphics.close()

    def bot_play(self):
        typeOfPlay = 2#cette variable (modifiée à la main) détermine comment le bot joue (0:aléatoire,1:minimax,2:alpha_beta)
        if typeOfPlay == 0 or self.gridListener.first[1]:
            piece = self.piecesPlayer[1][randint(0,len(self.piecesPlayer[1])-1)]
            self.selectedPiece = self.get_graphic_piece_by_piece(piece)
            self.gridListener.update_possibilities(self.player,self.selectedPiece.get_version())
            i = 0
            while len(self.gridListener.possibilities[self.player]) == 0:
                piece = self.piecesPlayer[1][randint(0, len(self.piecesPlayer[1]) - 1)]
                self.selectedPiece = self.get_graphic_piece_by_piece(piece)
                self.gridListener.update_possibilities(self.player, self.selectedPiece.get_version())
                i += 1
                if i > 24:
                    self.check_win(self.player)
                    break
            case = self.gridListener.possibilities[self.player][randint(0,len(self.gridListener.possibilities[self.player])-1)]
            self.place_piece(case)
            self.graphics.gridGraphics.add_piece(self.selectedPiece.piece, self.selectedPiece.version + 1,case, self.player)
            self.change_player()
            return
        if typeOfPlay == 1:
            m = opti.minimax(self.piecesPlayer, self.gridListener, opti.heuristique_bourrin, self.player, True, 2)
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
            return
        if typeOfPlay == 2:
            m = opti.alpha_beta(self.piecesPlayer, self.gridListener, opti.heuristique_pieces, self.player,self.player ,True, 1)
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
            return

class GraphicPiece:#Objet "pièce graphique",pièces bleuesà droite pour choisir la pièce à jouer
    def __init__(self,piece,game):
        self.piece = piece
        self.game = game
        self.widget = QWidget()
        self.grid = QGridLayout()
        self.version = 0
        self.versions = [t for t in piece.values()]
        self.rects = []
        self.clickable = [True,True]

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

    def click(self):
        if self.clickable[self.game.player]:
            self.game.selectedPiece = self
            self.bright()
            self.game.graphics.gridGraphics.clean_possibilities()
            self.game.gridListener.update_possibilities(self.game.player,self.game.selectedPiece.get_version())
            self.game.graphics.gridGraphics.show_possibilities(self.game.gridListener.possibilities[self.game.player])
            for p in self.game.pieces:
                if p != self and p.clickable[self.game.player]:p.dark()
    def show_possibilities(self,bot):
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
    def change_version(self):#fonction qui change la version de la pièce,appelée quand on apuie sur "v"
        self.version = (self.version+1)%len(self.versions)
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
g = Game(False)
sys.exit(app.exec_())






