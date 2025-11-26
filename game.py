from grid import Grid
import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QLabel,QGraphicsRectItem
import sys
from PyQt5.QtCore import Qt

class Game:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gridPlayer1 = Grid(14,14)
        self.gridPlayer2 = Grid(14, 14)
        self.gridGraphics = Grid(14, 14)

        container = QWidget()
        mainHbox = QHBoxLayout()
        rightVBox = QVBoxLayout()
        piecesVBox = QVBoxLayout()

        container.setLayout(mainHbox)

        player_label = QLabel("Jean marie le pen")
        player_label.setStyleSheet("""
                            QLabel{
                                font : Trebuchet MS;
                                color : pink;
                                font-weight:bold;
                            }
        
                                    """)
        rightVBox.addWidget(player_label)
        rightVBox.addLayout(piecesVBox)

        for i in range(10):
            piecesVBox.addLayout(self.get_graphic_piece(((0, 0), (0, 1))))

        mainHbox.addWidget(self.gridGraphics.grid)
        mainHbox.addLayout(rightVBox)
        container.show()

        self.app.exec()

    def get_graphic_piece(self,piece):
        vbox = QVBoxLayout()
        list = [(4-t[0],t[1]) for t in piece]
        for i in range(5):
            hbox = QHBoxLayout()
            for a in range(5):
                rect = QLabel()
                rect.setFixedSize(10,10)
                if (i,a) in list:
                    rect.setStyleSheet("""
                                                   QLabel{
                                                       border:1px;
                                                       border_color:black;
                                                       background-color:pink;
                                                       padding:0px;
                                                       margin:0px;
                                                   }
                                   """)
                else:
                    rect.setStyleSheet("""
                                                   QLabel{
                                                       background-color:black;
                                                       padding:0px;
                                                        margin:0px;
                                                   }
                                   """)
                hbox.addWidget(rect)
            hbox.setSpacing(0)
            hbox.setContentsMargins(0, 0, 0, 0)
            vbox.addLayout(hbox)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)

        return vbox

g = Game()





