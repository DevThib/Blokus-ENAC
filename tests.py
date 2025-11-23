import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

app = QApplication(sys.argv)
container = QWidget()
vbox = QVBoxLayout()
container.setLayout(vbox)
container.setGeometry(300, 300, 300, 300)
b = QPushButton("juif")
vbox.addWidget(b)
container.show()
app.exec()