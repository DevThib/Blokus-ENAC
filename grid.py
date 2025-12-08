import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout,QGridLayout
import sys
from PyQt5.QtCore import Qt

class Grid:

    def __init__(self, width, height,game):
        self.width = width
        self.height = height
        self.mat = np.zeros((width, height))
        self.cases = []
        self.grid = self.build_grid()
        self.game = game

    def build_grid(self):
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
    def add_piece(self, piece, pos,player):
        for t in piece:
            if pos[0]+t[0] < self.width and pos [1]+t[1]< self.height:
                self.mat[pos[0]+t[0],pos[1]+t[1]] = player+1
                case = self.cases[(pos[0]+t[0])*self.height+(pos[1]+t[1])]
                case.change_color(player)
                case.clickable = False

class Case:
    def __init__(self,x,y,grid):
        self.button = self.create_button()
        self.x = x
        self.y = y
        self.grid = grid
        self.clickable = True

    def create_button(self):
        b = QPushButton()
        b.clicked.connect(self.on_clicked)
        b.setFixedSize(50, 50)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setStyleSheet("""
                                          QPushButton {
                                              background-color: rgb(150,150,150);
                                              border:2.5px solid rgb(100,100,100);
                                          }
                                          QPushButton:hover{
                                            background-color: rgb(120,120,120);
                                            border:2.5px solid rgb(255,151,0);
                                          }
                                                 """)

        return b

    def on_clicked(self):
        if self.clickable:
            self.grid.add_piece(self.grid.game.selectedPiece.piece[self.grid.game.selectedPiece.version+1],(self.x,self.y),self.grid.game.player)

    def change_color(self,player):
        if player == 0:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                                                      QPushButton {
                                                          border: 1px solid rgb(225,131,0);
                                                          background-color:rgb(255,151,0);
                                                      }
                                                             """)
        else:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                                                                  QPushButton {
                                                                      border: 1px solid rgb(225,131,0);
                                                                      background-color:rgb(255,151,0);
                                                                  }
                                                                         """)