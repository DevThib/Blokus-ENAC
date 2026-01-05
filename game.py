from grid import Grid
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont, QKeyEvent
import sys
import automatisation as auto
from PyQt5.QtCore import Qt, QObject
from random import randint

import init_plateau as init
import possibilites_jeu_version as poss
import pose_version as placing
import debut_partie as starting
import clicable as clic

import new_variations as v

class GameGraphics(QMainWindow):
    def __init__(self,game):
        super().__init__()
        self.game = game

        self.gridGraphics = Grid(14, 14,game)

        self.container = QWidget(objectName = "test")
        mainHbox = QHBoxLayout()
        rightVBox = QVBoxLayout()
        piecesGrid = QGridLayout()

        self.container.setLayout(mainHbox)

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
        self.game.pieces[0].show_possibilities(False)
        self.game.pieces[0].click()
        piecesGrid.setSpacing(0)

        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)
        self.container.setStyleSheet("background-color:rgb(117,117,143);")
        self.container.setStyleSheet("""
                             QWidget#test{
                                    background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(87, 199, 133), stop:1 rgb(237, 221, 83));;
                                }
                                
        
        """)
        self.container.show()
        self.setCentralWidget(self.container)
        self.setFixedSize(self.container.size())

    def update_pieces(self,player):
        for p in self.game.pieces:
            p.set_visible(p.piece in self.game.piecesPlayer[player])

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            key_text = event.text()
            if key_text == "z":
                self.game.selectedPiece.change_version()
            if key_text == "j":
                self.game.change_player()
            if key_text == "m":
                print(self.game.gridListener.grids[0])

    def change_background_color(self,player):
        if player == 0:
            self.container.setStyleSheet("""
                                         QWidget#test{
                                                background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(87, 199, 133), stop:1 rgb(237, 221, 83));;
                                            }""")
        else:
            self.container.setStyleSheet("""
                                         QWidget#test{
                                                background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(255, 129, 0), stop:1 rgb(71, 212, 202));;
                                            }""")
class Game:
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
        self.check_win()


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

    def check_win(self):
        #vérifie la victoire du joueur opposé a celui qui vient de jouer
        #on teste toute les cases restantes,si aucune n'a de possibilités alors c'est gagné
        impossible = 0
        for piece in self.piecesPlayer[self.player]:
            self.get_graphic_piece_by_piece(piece).show_possibilities(True)
            if len(self.gridListener.possibilities[self.player]) == 0:
                impossible += 1
        if impossible == len(self.piecesPlayer[self.player]):
            print(f"Joueur {(self.player + 1) % 2} à gagné !!")
            self.graphics.close()

    def bot_play(self):
        piece = self.piecesPlayer[1][randint(0,len(self.piecesPlayer[1])-1)]
        self.selectedPiece = self.get_graphic_piece_by_piece(piece)
        self.selectedPiece.show_possibilities(True)
        i = 0
        while len(self.gridListener.possibilities[self.player]) == 0:
            piece = self.piecesPlayer[1][randint(0, len(self.piecesPlayer[1]) - 1)]
            self.selectedPiece = self.get_graphic_piece_by_piece(piece)
            self.selectedPiece.show_possibilities(True)
            i += 1
            if i > 24:
                self.check_win()
                break
        case = self.gridListener.possibilities[self.player][randint(0,len(self.gridListener.possibilities[self.player])-1)]
        self.place_piece(case)
        self.graphics.gridGraphics.add_piece(self.selectedPiece.piece, self.selectedPiece.version + 1,case, self.player)
        self.change_player()
        self.selectedPiece.show_possibilities(False)

class GraphicPiece:
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
            self.show_possibilities(False)
            for p in self.game.pieces:
                if p != self and p.clickable[self.game.player]:p.dark()
    def show_possibilities(self,bot):
        if not bot:
            try:
                for p in self.game.gridListener.possibilities[self.game.player]:
                    self.game.graphics.gridGraphics.grey_border_case(p)
            except AttributeError as e:
                pass
        self.game.gridListener.update_possibilities(self.game.player, self.game.selectedPiece.get_version())
        if not bot:
            try:
                for p in self.game.gridListener.possibilities[self.game.player]:
                    self.game.graphics.gridGraphics.dark_border_case(p)
            except AttributeError:
                pass

    def bright(self):
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                                                                     QPushButton{
                                                                         border: 1px solid rgb(225,131,0);
                                                                         background-color:rgb(255,151,0);
                                                                     }
                                                     """)
    def dark(self):
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                                                                     QPushButton{
                                                                         border: 1px solid rgb(0,0,100);
                                                                         background-color:blue;
                                                                     }
                                                     """)
    def change_version(self):
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

        self.show_possibilities(False)

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
g = Game(True)
sys.exit(app.exec_())






