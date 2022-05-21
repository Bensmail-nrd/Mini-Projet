from codecs import decode
import os
import re
import sys
import threading
from PySide2.QtGui import QColor
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from subprocess import Popen

import requests
from io import BytesIO
from pytube import *
import sqlite3



class Model(QWidget):
    def __init__(self):
        super(Model, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "main.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100,50,500,600)
        self.setWindowTitle("Youtube")
        self.grid = QGridLayout()
        self.grid.setRowMinimumHeight(0,400)
        self.grid.setRowMinimumHeight(1,60)
        self.list = self.findChild(QListWidget,"listWidget")
        self.leaveBtn = self.findChild(QPushButton,"leaveBtn")
        self.leaveBtn.clicked.connect(self.leave)
        self.grid.addWidget(self.list,row=0)
        self.grid.addWidget(self.leaveBtn,row=1)
        self.setLayout(self.grid)
        self.list.itemClicked.connect(self.itemClicked)
        self.getRecentFiles()
        self.show()
        thread = threading.Thread(target=self.setImages)
        thread.daemon=True
        thread.start()
        print("the thread just start")

        # self.list.setItemWidget(t,w)
    def itemClicked(self,item):
        path = "C:\\Program Files\\Google\\Chrome\\Application"
        url = item.data(Qt.UserRole)
        os.chdir(path)
        os.system("chrome "+ "\"" + url + "\"")
        # os.system("cd "+path +"\\chrome " + url )
    def leave(self):
        self.close()
    def getRecentFiles(self):
        con = sqlite3.connect('C:\\Users\\Baaziz Tarek\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
        cursor = con.cursor()
        cursor.execute("SELECT url,title,visit_count FROM urls ORDER BY visit_count DESC")
        self.urls = cursor.fetchall()
        con.close()
        self.l= []
        for i in self.urls:
            if "youtube.com/watch" in i[0].lower() :
                print("get a vedio")
                t = QListWidgetItem()
                self.l.append(t)
                t.setSizeHint(QSize(150, 80))
                t.setBackgroundColor(QColor(255, 248, 211))
                t.setText(i[1])
                t.setData(Qt.UserRole,i[0])
                t.setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
                self.list.setIconSize(QSize(100,100))
                self.list.addItem(t)
    
    def setImageForItem(self,item,image):
        self.l[item].setIcon(QIcon(QPixmap(image)))

    def setImages(self):
        img = QImage()
        k = 0
        for i in self.urls :
            if "youtube.com/watch" in i[0].lower() :
                try:
                    v = YouTube(i[0])
                    response = requests.get(v.thumbnail_url)
                    img.loadFromData(response.content)
                    print(f"get the image for index {k}")
                    self.l[k].setIcon(QIcon(QPixmap(img)))
                except:
                    print(f"lost the image for index {k}")
                k+=1

app = QApplication(sys.argv)
main = Model()
sys.exit(app.exec_())
