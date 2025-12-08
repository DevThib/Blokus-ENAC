from grid import Grid
import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont, QKeyEvent
import sys
import main as m
from PyQt5.QtCore import Qt,pyqtSignal

class Game:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()

        #self.gridPlayer1 = Grid(14,14)
        #self.gridPlayer2 = Grid(14, 14)
        self.gridGraphics = Grid(14, 14)
        self.selectedPiece = None
        self.pieces = []

        self.main_window.setStyleSheet("background-color:yellow;")

        container = QWidget()
        mainHbox = QHBoxLayout()
        rightVBox = QVBoxLayout()
        piecesGrid = QGridLayout()

        container.setLayout(mainHbox)

        player_label = QLabel("Joueur 1")
        player_label.setFixedSize(500,240)
        player_label.setStyleSheet("""
                            QLabel{
                                color : red;
                                font-weight:bold;
                            }
        
                                    """)
        player_label.setFont(QFont('Comic Sans MS', 60))
        player_label.setAlignment(Qt.AlignCenter)

        rightVBox.addWidget(player_label)
        rightVBox.addLayout(piecesGrid)

        i,j = 0,0
        for piece in m.pieces:
            p = GraphicPiece(piece,self)
            self.pieces.append(p)
            piecesGrid.addWidget(p.widget,i,j)
            j += 1
            if j == 5:
                i += 1
                j = 0
        self.selectedPiece = self.pieces[0]

        piecesGrid.setSpacing(0)

        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)

        container.setStyleSheet("background-color:rgb(210,210,210);")
        #container.setFixedSize(self.main_window.size())
        container.show()

        self.main_window.keyPressEvent = self.keyPressEvent

        #self.main_window.setFixedSize(self.main_window.size())
        self.app.exec()

    def keyPressEvent(self, event):
        if isinstance(event, QKeyEvent):
            key_text = event.text()
            print(key_text)
            self.selectedPiece.change_version()
class GraphicPiece:
    def __init__(self,piece,game):
        self.piece = piece
        self.game = game
        self.widget = QWidget()
        self.grid = QGridLayout()
        self.version = 0
        self.versions = [t for t in piece.values()]
        self.rects = []

        for i in range(5):
            for a in range(5):
                rect = QPushButton()
                rect.setFixedSize(15, 15)
                if (i, a) in self.versions[self.version]:
                    rect.setStyleSheet("""
                                                         QPushButton{
                                                             border: 1px solid rgb(0,0,200);
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
        self.game.selectedPiece = self
        self.bright()
        for p in self.game.pieces:
            if p != self:p.dark()
    def bright(self):
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                                                                     QPushButton{
                                                                         border: 1px solid rgb(200,0,0);
                                                                         background-color:red;
                                                                     }
                                                     """)
    def dark(self):
        for r in self.rects:
            if r[1]:r[0].setStyleSheet("""
                                                                     QPushButton{
                                                                         border: 1px solid rgb(0,0,200);
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
                                                             border: 1px solid rgb(0,0,200);
                                                             background-color:blue;
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




g = Game()





