from grid import Grid
import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont, QKeyEvent
import sys
import main as m
from PyQt5.QtCore import Qt

class GameGraphics(QMainWindow):
    def __init__(self,game):
        super().__init__()
        self.game = game

        self.gridGraphics = Grid(14, 14,game)

        self.container = QWidget()
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
        for piece in m.pieces:
            p = GraphicPiece(piece, self.game)
            self.game.add_piece(p)
            piecesGrid.addWidget(p.widget, i, j)
            j += 1
            if j == 5:
                i += 1
                j = 0
        self.game.set_selected_piece(self.game.pieces[0])
        self.game.pieces[0].click()
        piecesGrid.setSpacing(0)

        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)

        self.container.setStyleSheet("background-color:rgb(117,117,143);")
        self.container.show()

        self.setCentralWidget(self.container)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

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
                print(self.game.grids[0])

    def change_background_color(self,player):
        if player == 0:
            self.container.setStyleSheet("background-color:rgb(117,117,143);")
        else:
            self.container.setStyleSheet("background-color:rgb(117,143,130);")

class Game:
    def __init__(self):
        self.player = 0
        self.pieces = []
        self.selectedPiece = None
        self.graphics = GameGraphics(self)

        self.grids = (np.zeros((14, 14)),np.zeros((14, 14)))
        self.piecesPlayer = ([p for p in m.pieces],[p for p in m.pieces])

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

    def get_graphic_piece_by_piece(self,piece):
        for p in self.pieces:
            if p.piece == piece:
                return p

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
        self.grid.setSpacing(0)

    def click(self):
        if self.clickable[self.game.player]:
            self.game.selectedPiece = self
            self.bright()
            for p in self.game.pieces:
                if p != self and p.clickable[self.game.player] == True:p.dark()
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

app = QApplication(sys.argv)
g = Game()
sys.exit(app.exec_())






