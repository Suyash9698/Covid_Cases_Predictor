from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import QRect

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title="Self Assessment"
        # self.left = 300
        # self.top = 200
        # self.width = 300
        # self.height= 200
        self.ag = QDesktopWidget().availableGeometry()
        self.sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        self.x = int(0.8 * self.ag.width() - widget.width())
        self.y = int(0.2 * self.ag.height() - self.sg.height() - widget.height())

        # window.move(400,100)

        self.icon="icon.png"
        self.InitWindow()
    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top,self.x,self.y)
        self.move(self.x,self.y)
        self.setFixedWidth(480)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.show()
        self.Assess()
    def Assess(self):
        vbox = QVBoxLayout()
        #Groupbox1
        self.groupbox1 = QGroupBox("Select the symptoms if you have any of these:")
        self.groupbox1.setFont(QtGui.QFont("Sanserif", 11))
        vbox.addWidget(self.groupbox1)
        vbox1=QVBoxLayout()
        self.check1 = QCheckBox("Fever")
        vbox1.addWidget(self.check1)
        self.check1.toggled.connect(self.onCheck1)
        self.check2 = QCheckBox("Cold")
        vbox1.addWidget(self.check2)
        self.check2.toggled.connect(self.onCheck1)
        self.check3 = QCheckBox("Breathing Problem")
        vbox1.addWidget(self.check3)
        self.check3.toggled.connect(self.onCheck1)
        self.check4 = QCheckBox("None of the above")
        vbox1.addWidget(self.check4)
        self.check4.toggled.connect(self.onCheck1)
        self.button1 = QPushButton("Next")
        self.button1.clicked.connect(self.btn_click1)
        vbox1.addWidget(self.button1)
        self.button1.setEnabled(False)
        self.groupbox1.setLayout(vbox1)

        #Groupbox2
        self.groupbox2 = QGroupBox("Are you a patient of any of the following disease?")
        self.groupbox2.setFont(QtGui.QFont("Sanserif", 11))

        vbox2 = QVBoxLayout()
        vbox.addWidget(self.groupbox2)
        self.check5 = QCheckBox("Diabetes")
        vbox2.addWidget(self.check5)
        self.check5.toggled.connect(self.onCheck2)
        self.check6 = QCheckBox("High blood pressure")
        vbox2.addWidget(self.check6)
        self.check6.toggled.connect(self.onCheck2)
        self.check7 = QCheckBox("Kidney infection ")
        vbox2.addWidget(self.check7)
        self.check7.toggled.connect(self.onCheck2)
        self.check8 = QCheckBox("None of the above")
        vbox2.addWidget(self.check8)
        self.check8.toggled.connect(self.onCheck2)
        self.button2 = QPushButton("Next")
        vbox2.addWidget(self.button2)
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.btn_click2)
        self.button2.toggled.connect(self.onCheck2)
        self.groupbox2.setLayout(vbox2)
        self.groupbox2.setVisible(False)

        #Groupbox3
        self.groupbox3= QGroupBox("Do you have any international travel history in past 30 days?")
        self.groupbox3.setFont(QtGui.QFont("Sanserif", 11))

        vbox3 = QVBoxLayout()
        vbox.addWidget(self.groupbox3)
        self.check9 = QCheckBox("Yes")
        vbox3.addWidget(self.check9)
        self.check9.toggled.connect(self.onCheck3)
        self.check10 = QCheckBox("No")
        vbox3.addWidget(self.check10)
        self.check10.toggled.connect(self.onCheck3)
        self.button3= QPushButton("Next")
        vbox3.addWidget(self.button3)
        self.button3.setEnabled(False)
        self.button3.clicked.connect(self.btn_click3)
        self.button3.toggled.connect(self.onCheck3)

        self.groupbox3.setLayout(vbox3)
        self.groupbox3.setVisible(False)

        #Groupbox4
        self.groupbox4 = QGroupBox("Which of the following apply to you?")
        self.groupbox4.setFont(QtGui.QFont("Sanserif", 11))

        vbox4 = QVBoxLayout()
        vbox.addWidget(self.groupbox4)
        self.check11 = QCheckBox("I have come in contact of corona positive")
        vbox4.addWidget(self.check11)
        self.check11.toggled.connect(self.onCheck4)
        self.check12 = QCheckBox("I am a health worker")
        vbox4.addWidget(self.check12)
        self.check12.toggled.connect(self.onCheck4)
        self.check13= QCheckBox("None of the above")
        vbox4.addWidget(self.check13)
        self.check13.toggled.connect(self.onCheck4)
        self.button4 = QPushButton("Submit details")
        vbox4.addWidget(self.button4)
        self.button4.setEnabled(False)
        self.button4.clicked.connect(self.onClick)
        self.button4.toggled.connect(self.onCheck4)
        self.groupbox4.setLayout(vbox4)
        self.groupbox4.setVisible(False)
        self.setLayout(vbox)
    def onCheck1(self):
        if (self.check1.isChecked() == True or self.check2.isChecked() == True or self.check3.isChecked() == True ):
            self.check4.setEnabled(False)
        if(self.check4.isChecked()==True):
            self.check1.setEnabled(False)
            self.check2.setEnabled(False)
            self.check3.setEnabled(False)
        if(self.check1.isChecked() == True or self.check2.isChecked() == True or self.check3.isChecked() == True or
        self.check4.isChecked() == True):
            self.button1.setEnabled(True)
        else:
            self.check4.setEnabled(True)
            self.button1.setEnabled(False)
            self.check1.setEnabled(True)
            self.check2.setEnabled(True)
            self.check3.setEnabled(True)
    def onCheck2(self):
        if (self.check5.isChecked() == True or self.check6.isChecked() == True or self.check7.isChecked() == True ):
            self.check8.setEnabled(False)
        if (self.check8.isChecked() == True):
            self.check5.setEnabled(False)
            self.check6.setEnabled(False)
            self.check7.setEnabled(False)
        if(self.check5.isChecked() == True or self.check6.isChecked() == True or self.check7.isChecked() == True or
        self.check8.isChecked() == True):
            self.button2.setEnabled(True)
        else:
            self.check8.setEnabled(True)
            self.button2.setEnabled(False)
            self.check5.setEnabled(True)
            self.check6.setEnabled(True)
            self.check7.setEnabled(True)
    def onCheck3(self):
        if (self.check9.isChecked() == True):
            self.check10.setEnabled(False)
        if (self.check10.isChecked() == True):
            self.check9.setEnabled(False)
        if(self.check9.isChecked() == True or self.check10.isChecked() == True):
            self.button3.setEnabled(True)
        else:
            self.check10.setEnabled(True)
            self.button3.setEnabled(False)
            self.check9.setEnabled(True)
    def onCheck4(self):
        if (self.check11.isChecked() == True or self.check12.isChecked() == True):
            self.check13.setEnabled(False)
        if (self.check13.isChecked() == True):
            self.check11.setEnabled(False)
            self.check12.setEnabled(False)
        if(self.check11.isChecked() == True or self.check12.isChecked() == True or self.check13.isChecked() == True):
            self.button4.setEnabled(True)
        else:
            self.check13.setEnabled(True)
            self.button4.setEnabled(False)
            self.check11.setEnabled(True)
            self.check12.setEnabled(True)
    def btn_click1(self):
            self.groupbox2.setVisible(True)
            self.groupbox1.setEnabled(False)

    def btn_click2(self):
            self.groupbox3.setVisible(True)
            self.groupbox2.setEnabled(False)
    def btn_click3(self):
            self.groupbox4.setVisible(True)
            self.groupbox3.setEnabled(False)
    def onClick(self):
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon("download.png"))
            msg.setWindowTitle("Assessment Result")
    
            # Calculate the position to center the message box
            msg_geometry = msg.frameGeometry()
            center_point = QDesktopWidget().availableGeometry().center()
            msg_geometry.moveCenter(center_point)
            msg.move(msg_geometry.topLeft())
    
            if (self.check1.isChecked() == True and self.check2.isChecked() == True and self.check3.isChecked() == True and
               (self.check5.isChecked() == True or self.check6.isChecked() == True or self.check7.isChecked() == True) and
               self.check9.isChecked() == True and (self.check11.isChecked() == True or self.check12.isChecked() == True)):

                    msg.setText("If the information provided by you is accurate, it indicates that you are either unwell or at high risk. "
                        "Your test results and location history need to be sent to the health ministry to help you and help "
                        "identify hotspots where infection may be spreading.")
            elif (self.check4.isChecked() == True and self.check8.isChecked() == True and self.check10.isChecked() == True and
                        self.check13.isChecked()):
                    msg.setText("Your infection risk is low. We recommend that you stay at home to avoid any chance of exposure "
                        "to the novel coronavirus.")
            else:
                    msg.setText("You may have a risk of corona. It is advised to have a checkup for novel coronavirus.")
    
            msg.exec_()
            self.close()



# if __name__ == '__main__':
#      app=QApplication(sys.argv)

#      window=Window()
#      window.ag = QDesktopWidget().availableGeometry()
#      window.sg = QDesktopWidget().screenGeometry()
#      widget = window.geometry()
#      x = 0.5 * window.ag.width() - widget.width()
#      y = 1 * window.ag.height() - window.sg.height() - widget.height()

#      #window.move(400,100)
#      window.move(x, y)
#      sys.exit(app.exec())
