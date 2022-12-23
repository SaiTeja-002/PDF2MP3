import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)
        self.resize(800,700)
        self.setWindowTitle("PDF2MP3")
        self.label = QLabel(self)
        self.label.setText("This is the text")
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)

        self.label.setFont(font)
        self.label.move(200,20)

        font.setPointSize(30)
        self.label30 = QLabel(self)
        self.label30.setText("Text Size 30 BAM!!!")

        self.label30.setFont(font)
        self.label30.move(200, 100)
    



def main():
   app = QApplication(sys.argv)
   ex = window()
   ex.show()
   sys.exit(app.exec_())


if __name__ == '__main__':
   main()