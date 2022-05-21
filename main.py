import datetime
import sys
import os
import sys
from ipaddress import IPv4Address

# from pyairmore.request import AirmoreSession
# from pyairmore.services.messaging import (MessageRequestGSMError,
#                                           MessagingService)
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from AutoCompletion import AutoCompleteLineEdit

ip = "192.168.137.125"

from PySide2.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QListWidgetItem
)
#from PyQt5.uic import loadUi
from fee import Ui_MainWindow

import requests
import time

from main2 import messageWidget, ITEM
# def getMessagesHistory(ipAddress):
#     ip = IPv4Address(ipAddress)
#     session = AirmoreSession(ip)
#     service = MessagingService(session)
#     return service.fetch_message_history()

# def getMessagesChat(ipAddress,id):
#     ip = IPv4Address(ipAddress)
#     session = AirmoreSession(ip)
#     service = MessagingService(session)
#     return service.fetch_chat_history(id,0,100)


# def sendMessage(ipAddress,msg,num):
#     ip = IPv4Address(ipAddress)
#     session = AirmoreSession(ip)
#     service = MessagingService(session)
#     try :
#         service.send_message(num,msg)
#     except MessageRequestGSMError:
#         print(MessageRequestGSMError)
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



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.i=1
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.apps.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3))
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        #self.ui.pushButton_8.clicked.connect(self.shaw)
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_2))
        self.ui.parametre.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_4))
        self.ui.info.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_5))
        self.ui.message.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_6))
        # chat = getMessagesHistory(ip)
        # for i in chat:
        #     temp = QListWidgetItem()
        #     temp.setSizeHint(QSize(200, 100))
        #     if "RECEIVED" in str(i.type):
        #         icon = "arrow-1.png"
        #     else:
        #         icon = "arrow-2.png"
        #     wgd = messageWidget()
        #     wgd.set(i.id, i.name, i.phone, i.content, icon)
        #     self.l.addItem(temp)
        #     self.l.setItemWidget(temp, wgd)



    def shaw(self):
        if(self.i==1):
            city = "Alger"#textField.get()
            api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=5b01736f915a26cd6f3911ca945e442e"

            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))
            self.i=2
            final_info ="   "+ condition + "\n   " + str(temp) + "°C"
            final_data = "\n    " + "Min Temp: " + str(min_temp) + "°C" + "\n   " + "Max Temp: " + str(
            max_temp) + "°C" + "\n  " + "Pressure: " + str(pressure) + "\n  " + "Humidity: " + str(
            humidity) + "\n " + "Wind Speed: " + str(wind) + "\n    " + "Sunrise: " + sunrise + "\n " + "Sunset: " + sunset
            self.ui.label.setText(final_info+final_data)  # label1.config(text=final_info)

        while(True):
            QApplication.processEvents()
            dt=datetime.datetime.now()
            self.ui.date.setText('\n\n\n\t\t\t%s : %s: %s'%(dt.hour,dt.minute,dt.second))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
   # win.shaw()
    sys.exit(app.exec())