import subprocess
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton
import remarks



class Window2():
    def __init__(self):
        super().__init__()
    # import viewstar


class Wid(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Wid, self).__init__(parent)
        self.setGeometry(400, 100, 300, 300)


        hlay = QtWidgets.QHBoxLayout()
        hlay.addStretch(1)

        vlay = QtWidgets.QVBoxLayout(self)
        vlay.addStretch(1)

        self.chatbot = QPushButton(self)
        self.chatbot.setFixedHeight(250)
        self.chatbot.setFixedWidth(100)
        self.chatbot.clicked.connect(self.fun)

        # self.btn.clicked.connect(w.show)
        self.chatbot.installEventFilter(self)
        hlay.addWidget(self.chatbot)
        hlay.addStretch(1)

        vlay.addLayout(hlay)
        self.setLayout(vlay)

    def closeEvent(self, event):
        self.fun()

    def fun(self):
        self.close()
        self.s = remarks.WebPage()
        self.s.show()

    def eventFilter(self, obj, event):
        if obj == self.chatbot and event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered()
        return super(Wid, self).eventFilter(obj, event)

    def onHovered(self):
        # print("hovered")
        subprocess.call(["say", "-v", "Samantha", "Hello"])


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = Wid()
    w.show()
    sys.exit(app.exec_())
