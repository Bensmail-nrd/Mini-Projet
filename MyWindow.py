import sys
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.load_ui()
    def load_ui(self):
        uic.loadUi('fee.ui', self)
        self.message.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(4))



app = QApplication(sys.argv)
main = Main()
main.show()
sys.exit(app.exec_())