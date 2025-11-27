import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QGridLayout
import sys
from PyQt5.QtCore import Qt

class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mat = np.zeros((width, height))
        self.buttons = [[] for _ in range(height)]
        self.grid = self.build_grid()

    def build_grid(self):
        container = QWidget()
        gridLayout = QGridLayout()
        container.setLayout(gridLayout)

        gridLayout.setSpacing(0)
        def p():
            print("test")

        for i in range(self.height):
            for a in range(self.width):
                b = QPushButton()
                b.clicked.connect(p)
                b.setFixedSize(50, 50)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setStyleSheet("""
                           QPushButton {
                               background-color: rgb(150,150,150);
                               border:2.5px solid rgb(100,100,100);
                           }
                           QPushButton:hover{
                            background-color: rgb(120,120,120);
                           }
                                  """)
                gridLayout.addWidget(b,i,a)
                self.buttons[i].append(b)
        return container
    def add_piece(self, piece, pos,player):
        for t in piece:
            self.mat[pos[0]+t[0],pos[1]+t[1]] = player
            b = self.buttons[pos[0]+t[0]][pos[1]+t[1]]
            b.setCursor(Qt.CursorShape.ArrowCursor)
            b.setStyleSheet("""
                                                                                           QPushButton {
                                                                                               background-color: blue;
                                                                                               border:5px solid;
                                                                                               border-color:black;
                                                                                           }
                                                                                                  """)


