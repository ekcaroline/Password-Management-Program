import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        
        layout = QVBoxLayout()

        button1 = QPushButton("button 1")
        button1.clicked.connect(lambda: self.pressed(1))
        
        button2 = QPushButton("button 2")
        button2.clicked.connect(lambda: self.pressed(2))
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def pressed(self, buttonNumber):
        print("button", buttonNumber, "Clicked!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()