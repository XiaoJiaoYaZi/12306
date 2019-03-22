import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent, QPainter, QPaintEvent, QCursor

from window.PyUI.UI_Capture import Ui_Capture

class CCapture(QtWidgets.QDialog,Ui_Capture):
    def __init__(self,parent=None):
        super(CCapture,self).__init__(parent=parent)
        self.setupUi(self)
        #self.img = QPixmap.fromImage(QImage.fromData(buffer))
        self.img = QPixmap(os.getcwd() + "/12306.jpg")
        self.__initUI()
        self.__connections()

    def __initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._train = QPixmap(os.getcwd()+"/railway_station.png")
        self.painter = QPainter(self.img)
        self.label.setPixmap(self.img)
        self._positon = []

    def __drawtrain(self,x,y):
        self.painter.drawPixmap(x,y,self._train)
        self.label.setPixmap(self.img)

    def __drawrestore(self):
        self.painter.restore()
        self.label.setPixmap(self.img)

    def __connections(self):
        self.buttonBox.rejected.connect(self.close)

    def mousePressEvent(self, a0: QMouseEvent):
        if self.label.geometry().contains(QCursor.pos()):
            if(a0.type() == QMouseEvent.MouseButtonPress and a0.button()== Qt.RightButton):
                x = a0.x()-self.label.pos().x()-13
                y = a0.y()-self.label.pos().y()-13
                self.__drawtrain(x,y)
                self._positon.append('{},{}'.format(x, y - 29))
                print(self._positon)

    @property
    def positions(self):
        return self._positon






if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ex = CCapture()
    ex.show()
    sys.exit(app.exec_())