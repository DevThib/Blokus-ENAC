import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
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
        vbox = QVBoxLayout()
        container.setLayout(vbox)
        def p():
            print("test")

        for i in range(self.height):
            hbox = QHBoxLayout()
            for a in range(self.width):
                b = QPushButton()
                b.clicked.connect(p)
                b.setFixedSize(50, 50)
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.setStyleSheet("""
                           QPushButton {
                               background-color: grey;
                               border:5px;
                               border-color:black;
                           }
                           QPushButton:hover{
                            background-color: white;
                           }
                                  """)
                hbox.addWidget(b)
                self.buttons[i].append(b)
            vbox.addLayout(hbox)
        return container
    def add_piece(self, piece, pos):
        for t in piece:
            self.mat[pos[0]+t[0],pos[1]+t[1]] = 1
            b = self.buttons[pos[0]+t[0]][pos[1]+t[1]]
            b.setCursor(Qt.CursorShape.ArrowCursor)
            b.setStyleSheet("""
                                                                                           QPushButton {
                                                                                               background-color: blue;
                                                                                               border:5px;
                                                                                               border-color:black;
                                                                                           }
                                                                                                  """)


