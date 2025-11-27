from grid import Grid
import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGridLayout,QMainWindow
from PyQt5.QtGui import QFont
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
        self.selectedPiece = m.piece_1

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
            piecesGrid.addWidget(self.get_graphic_piece(piece[1]),i,j)
            j += 1
            if j ==5:
                i += 1
                j = 0

        piecesGrid.setSpacing(0)


        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)

        container.setStyleSheet("background-color:rgb(210,210,210);")

        container.show()

        self.app.exec()

    def get_graphic_piece(self,piece):
        pieceWidget = QWidget()
        pieceLayout = QGridLayout()
        list = [(4-t[0],t[1]) for t in piece]
        rects = []

        def click():
            for i in range(5):
                for a in range(5):
                    if (i, a) in list:
                        rects[i*5+a].setStyleSheet("""
                                                           QPushButton{
                                                               background-color:red;
                                                               border: 1px solid rgb(200,0,0);
                                                           }
                                        """)
                    else:
                        rects[i*5+a].setStyleSheet("""
                                                           QPushButton{
                                                               background-color:transparent;
                                                           }
                                        """)
            self.selectedPiece = self.search_piece(piece)
            print(self.selectedPiece)
        for i in range(5):
            for a in range(5):
                rect = QPushButton()
                rect.setFixedSize(15,15)
                if (i,a) in list:
                    rect.setStyleSheet("""
                                                   QPushButton{
                                                       border: 1px solid rgb(0,0,200);
                                                       background-color:blue;
                                                   }
                                   """)
                else:
                    rect.setStyleSheet("""
                                                   QPushButton{
                                                       background-color:transparent;
                                                   }
                                   """)
                pieceLayout.addWidget(rect,i,a)
                pieceWidget.setLayout(pieceLayout)
                rects.append(rect)

        pieceWidget.setContentsMargins(0,0,0,0)
        pieceWidget.mousePressEvent = lambda event: click()

        pieceLayout.setSpacing(0)

        return pieceWidget

    def search_piece(self,piece):
        for p in m.pieces:
            if piece in p.values():
                return p

g = Game()





