import os
import sys
import threading
import cv2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QImage, QPixmap
import requests


class ITEM(QWidget):
    def __init__(self):
        super(ITEM, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__),"main1.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        self.zoom = 0
        self.frontCamera = False
        self.torchOn=False
        self.voicOn=False
        self.zoomInBtn = self.findChild(QPushButton,"zoomInBtn")
        self.zoomInBtn.clicked.connect(self.zoomIn)
        self.zoomOutBtn = self.findChild(QPushButton,"zoomOutBtn")
        self.zoomOutBtn.clicked.connect(self.zoomOut)
        self.flipBtn = self.findChild(QPushButton,"flipBtn")
        self.flipBtn.clicked.connect(self.flip)
        self.torchBtn = self.findChild(QPushButton,"torchBtn")
        self.torchBtn.clicked.connect(self.torch)
        self.voicBtn = self.findChild(QPushButton,"voicBtn")
        self.voicBtn.clicked.connect(self.voic)
        self.imgLabel = self.findChild(QLabel,"imgLabel")
        self.gridLayout = self.findChild(QGridLayout,"gridLayout")
        self.verticalLayout=self.findChild(QVBoxLayout,"verticalLayout")   

    def zoomIn(self):
        if self.zoom <100 :
            self.zoom+=10
        requests.get("http://192.168.145.86:8080/ptz?zoom={}".format(self.zoom))
        pass
    def zoomOut(self):
        if self.zoom >10 :
            self.zoom-=10
        else : 
            self.zoom=0
        requests.get("http://192.168.145.86:8080/ptz?zoom={}".format(self.zoom))
        pass
    def flip(self):
        if self.frontCamera:
            requests.get("http://192.168.145.86:8080/settings/ffc?set=on")
            self.frontCamera=False
        else:
            requests.get("http://192.168.145.86:8080/settings/ffc?set=off")
            self.frontCamera=True
    def torch(self):
        if self.torchOn:
            requests.get("http://192.168.145.86:8080/enabletorch")
            self.torchBtn.setText("torch off")
            self.torchOn=False
        else:
            requests.get("http://192.168.145.86:8080/disabletorch")
            self.torchBtn.setText("torch on")
            self.torchOn=True
    def voic(self):
        if self.voicOn:
            requests.get("http://192.168.145.86:8080/audio.opus")

    def display(self,image):
        qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0],qformat)
        outImage = outImage.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
        # self.imgLabel.setScaledContents(True)

# from selenium import webdriver
# driver = webdriver.Chrome()
# driver.get("http://192.168.146.108:8080/greet.html")
# driver.find_element("flashcb").click()

# cap2 = cv2.VideoCapture("http://192.168.125.235:8080/video")

# while(True):
#     ret, frame = cap.read()
#     # ret2, frame2 = cap2.read()
#     frame=cv2.resize(frame,(500,500))
#     # frame2=cv2.resize(frame2,(500,500))
#     cv2.imshow('frame',frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
def doIt():
    cap = cv2.VideoCapture("http://192.168.145.86:8080/video")
    while(True):
        ret, frame = cap.read()
        main.display(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
app = QApplication(sys.argv)
main = ITEM()
main.show()
thread = threading.Thread(target=doIt)
thread.daemon = True
thread.start()
sys.exit(app.exec_())