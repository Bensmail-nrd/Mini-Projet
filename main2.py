from ctypes import alignment
import os
import sys
from ipaddress import IPv4Address


from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import (MessageRequestGSMError,
                                          MessagingService)
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtGui import *
 
from AutoCompletion import AutoCompleteLineEdit

ip = "192.168.43.32"

def getMessagesHistory(ipAddress):
    ip = IPv4Address(ipAddress)
    session = AirmoreSession(ip)
    service = MessagingService(session)
    return service.fetch_message_history()

def getMessagesChat(ipAddress,id):
    ip = IPv4Address(ipAddress)
    session = AirmoreSession(ip)
    service = MessagingService(session)
    return service.fetch_chat_history(id,0,100)


def sendMessage(ipAddress,msg,num):
    ip = IPv4Address(ipAddress)
    session = AirmoreSession(ip)
    service = MessagingService(session)
    try :
        service.send_message(num,msg)
    except MessageRequestGSMError:
        print(MessageRequestGSMError)

class messageWidget(QWidget):
    def __init__(self):
        super(messageWidget, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "messageWidget.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        self.nameLabel = self.findChild(QLabel,"name")
        self.numberLabel = self.findChild(QLabel,"number")
        self.contentLabel = self.findChild(QLabel,"content")
        self.icon = self.findChild(QLabel,"icon")
    def set(self,id,name,number,content,icon):
        self.selectedItem=id
        self.nameLabel.setText(name)
        self.numberLabel.setText(number)
        self.contentLabel.setText(content)
    def get(self):
        return self.selectedItem,self.nameLabel.text(),self.numberLabel.text(),self.contentLabel.text()




class ITEM(QWidget):
    def __init__(self):
        super(ITEM, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        self.frame = self.findChild(QFrame,"frame")       
        self.btnMSG = self.findChild(QPushButton,"pushButton_3")
        self.btnSND = self.findChild(QPushButton,"pushButton_4")
        self.btnSNDMSG = self.findChild(QPushButton,"sendMsgBtn")
        self.lineWidget = self.findChild(QWidget,"widget")
        self.lineEdit = AutoCompleteLineEdit(path="./list.txt",parent=self.lineWidget)
        self.lineEdit.setGeometry(0,0,400,20)
        self.btnSNDMSG.clicked.connect(self.sendMsgBtnClicked)
        self.btnLEAVE = self.findChild(QPushButton,"leave")
        self.btnLEAVE.clicked.connect(self.leaveClicked)
        self.btnMSG.clicked.connect(self.msgFunction)
        self.btnSND.clicked.connect(self.sendFunction)
        self.l = self.findChild(QListWidget,"listWidget")
        self.l2 = self.findChild(QListWidget,"listWidget_2")
        self.l.itemClicked.connect(self.clicked)
        self.stack = self.findChild(QStackedWidget,"stackedWidget")
        self.stack.setCurrentIndex(0)
        chat = getMessagesHistory(ip)
        for  i in chat:
            temp = QListWidgetItem()
            temp.setSizeHint(QSize(200,100))
            if "RECEIVED" in str(i.type):
                icon = "arrow-1.png"
            else :
                icon ="arrow-2.png"
            wgd=messageWidget()
            wgd.set(i.id,i.name,i.phone,i.content,icon)
            self.l.addItem(temp)
            self.l.setItemWidget(temp,wgd)
    def sendMsgBtnClicked(self):
        sendMessage(ip,self.lineEdit.text(),self.number)
        self.lineEdit.setText = ""
    def clicked(self,item):
        self.stack.setCurrentIndex(1)
        content = self.l.itemWidget(item).get()
        self.number = content[2]
        
        print(content[0])
        chat = getMessagesChat(ip,content[0])
        for i in chat:
            temp = QListWidgetItem()
            if "RECEIVED" in str(i.type):
                temp.setIcon(QIcon(QPixmap("./arrow-1.png")))
            else:
                temp.setIcon(QIcon(QPixmap("./arrow-2.png")))
            # temp.setSizeHint(QSize(200,80))
            temp.setText(i.content)
            temp.setTextAlignment(Qt.AlignTop)
            temp.setBackgroundColor(QColor(131, 212, 255))
            #wgd=messageWidget()
            #wgd.set(i.id,i.name,i.phone,i.content)
            self.l2.addItem(temp)
            #self.l2.setItemWidget(temp,wgd)
    def msgFunction(self):
        self.stack.setCurrentIndex(0)
        
    def sendFunction(self):
        pass
    def leaveClicked(self):
        self.stack.setCurrentIndex(0)
        self.l2.clear()     
        


    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type()==QEvent.Enter:
            pass     
        return super().eventFilter(watched, event)
        
    

