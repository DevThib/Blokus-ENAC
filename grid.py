import numpy as np
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
import sys
from PyQt5.QtCore import Qt


class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        app = QApplication(sys.argv)
        self.mat = np.zeros((width, height))
        self.grid = self.build_grid()

        app.exec()

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
                               transition: background-color 10s;
                           }
                           QPushButton:hover{
                            background-color: white;
                           }
                                  """)
                hbox.addWidget(b)
            vbox.addLayout(hbox)
        container.show()
        return container

    def add_piece(self, piece, pos):
        pass


g = Grid(10, 10)
