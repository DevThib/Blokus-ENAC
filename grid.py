import numpy as np
from PyQt5.QtWidgets import  QWidget, QPushButton,QGridLayout
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
    def add_piece(self, piece,version, pos,player):
        for t in piece[version]:
            if pos[0]+t[0] < self.width and pos [1]+t[1]< self.height:
                self.mat[pos[0]+t[0],pos[1]+t[1]] = player+1
                self.game.grids[player][pos[0]+t[0],pos[1]+t[1]] = player+1
                case = self.cases[(pos[0] + t[0]) * self.height + (pos[1] + t[1])]
                case.change_color(player)
                case.clickable = False
        self.game.remove_piece_for_player(player, piece)

    def get_coordinates(self,case):
        for i in range(len(self.cases)):
            if self.cases[i].button == case:
                return (i//self.width,i%self.width)

class Case:
    def __init__(self,x,y,grid):
        self.button = self.create_button()
        self.x = x
        self.y = y
        self.grid = grid
        self.clickable = True

    def create_button(self):
        class CaseButton(QPushButton):
            def __init__(self,case):
                super().__init__()
                self.clicked.connect(case.on_clicked)
                self.setFixedSize(50, 50)
                self.setCursor(Qt.CursorShape.PointingHandCursor)
                self.setStyleSheet("""
                                                  QPushButton {
                                                      background-color: rgb(150,150,150);
                                                      border:2.5px solid rgb(100,100,100);
                                                  }
                                                  
                                                         """)

                self.case = case
            def enterEvent(self, a0):
                pos = self.case.grid.get_coordinates(self)
                for c in self.case.grid.game.selectedPiece.piece[self.case.grid.game.selectedPiece.version+1]:
                    cb = self.case.grid.cases[(pos[0]+c[0])*self.case.grid.width+pos[1]+c[1]]
                    if cb.clickable:
                        cb.button.setStyleSheet("""
                                                                          QPushButton {
                                                                              background-color: rgb(150,150,150);
                                                                              border:2.5px solid orange;
                                                                          }
                                                                
                                                                                 """)
            def leaveEvent(self, a0):
                pos = self.case.grid.get_coordinates(self)
                for c in self.case.grid.game.selectedPiece.piece[self.case.grid.game.selectedPiece.version + 1]:
                    cb = self.case.grid.cases[(pos[0] + c[0]) * self.case.grid.width + pos[1] + c[1]]
                    if cb.clickable:
                        cb.button.setStyleSheet("""
                                               QPushButton {
                                                          background-color: rgb(150,150,150);
                                                          border:2.5px solid rgb(100,100,100);
                                                      }
    
                                                                                                 """)



        return CaseButton(self)

    def on_clicked(self):
        if self.clickable:
            self.grid.add_piece(self.grid.game.selectedPiece.piece,self.grid.game.selectedPiece.version+1,(self.x,self.y),self.grid.game.player)
            self.grid.game.change_player()
    def change_color(self,player):
        if player == 0:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                                                      QPushButton {
                                                          border: 1px solid rgb(0,90,0);
                                                          background-color:rgb(0,140,0);
                                                      }
                                                             """)
        else:
            self.button.setCursor(Qt.CursorShape.ArrowCursor)
            self.button.setStyleSheet("""
                                                                  QPushButton {
                                                                      border: 1px solid rgb(90,0,0);
                                                                      background-color:rgb(140,0,0);
                                                                  }
                                                                         """)