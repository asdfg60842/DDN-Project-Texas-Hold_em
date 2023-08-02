import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

form_class = uic.loadUiType("TexasHoldem/ui/untitled.ui")[0]

class MainClass(QMainWindow, form_class):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainClass()
    app.exec_()