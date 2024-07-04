from tkinter import END

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget, QApplication, QPushButton, QDesktopWidget
from bot_final import chat
import time
import threading
import subprocess
import qtawesome as qta

width = 496
height = 673


class ChatInterface(QtWidgets.QMainWindow):

    def __init__(self):
        super(ChatInterface, self).__init__()
        self.sent_label = QLabel(self)
        self.setGeometry(1420, 400, width, height)
        self.ag = QDesktopWidget().availableGeometry()
        self.sg = QDesktopWidget().screenGeometry()

        
        widget = self.geometry()
        x = int(self.ag.width() - widget.width())
        y = int(2.5 * self.ag.height() - self.sg.height() - widget.height())
        self.move(x, y)
        # self.setStyleSheet("padding:6px")
        self.setWindowTitle("COBOT")
        self.setFixedWidth(496)
        self.setFixedHeight(630)
        self.con = ""
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 546, 401, 41))
        # self.textEdit.setStyleSheet("QTextEdit { padding-left:6; padding-top:6; padding-bottom:10; padding-right:6}");

        # self.textEdit.setObjectName("textEdit")

        # button
        self.pushButton = QtWidgets.QPushButton('SEND', self)
        self.pushButton.setGeometry(QtCore.QRect(405, 546, 84, 41))

        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.send_message_insert)

        self.sent_label = QtWidgets.QLabel(self)
        self.last_sent_label(date="No messages sent.")

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setGeometry(QtCore.QRect(0, 15, 491, 526))
        self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 15, 489, 524))
        # self.scrollAreaWidgetContents.setStyleSheet("padding-top:10px")

        self.textBrowser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QtCore.QRect(0, 15, 491, 526))
        # self.textBrowser.setObjectName("textBrowser")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        mainMenu = self.menuBar()
        # self.mainMenu.setGeometry(QtCore.QRect(0, 0, 496, 26))

        # File
        FILE = mainMenu.addMenu("FILE")
        CLEAR_CHAT = FILE.addAction('CLEAR CHAT')
        CLEAR_CHAT.triggered.connect(self.clear_chat)
        EXIT = FILE.addAction('EXIT')
        EXIT.triggered.connect(self.chatexit)

        # options
        OPTIONS = mainMenu.addMenu("OPTIONS")

        FONT = OPTIONS.addMenu("FONT")

        DEFAULT2 = FONT.addAction("DEFAULT")
        DEFAULT2.triggered.connect(self.font_change_default)
        TIMES = FONT.addAction("TIMES")
        TIMES.triggered.connect(self.font_change_times)
        SYSTEM = FONT.addAction("SYSTEM")
        SYSTEM.triggered.connect(self.font_change_system)
        HELVETICA = FONT.addAction("HELVETICA")
        HELVETICA.triggered.connect(self.font_change_helvetica)
        FIXEDSYS = FONT.addAction("FIXEDSYS")
        FIXEDSYS.triggered.connect(self.font_change_fixedsys)

        # color theme
        COLOR_THEME = OPTIONS.addMenu("COLOR THEME")
        DEFAULT = COLOR_THEME.addAction("DEFAULT")
        DEFAULT.triggered.connect(self.color_theme_default)
        DARK = COLOR_THEME.addAction("DARK")
        DARK.triggered.connect(self.color_theme_dark)
        GREY = COLOR_THEME.addAction("GREY")
        GREY.triggered.connect(self.color_theme_grey)
        BLUE = COLOR_THEME.addAction("BLUE")
        BLUE.triggered.connect(self.color_theme_blue)
        TORQUE = COLOR_THEME.addAction("TORQUE")
        TORQUE.triggered.connect(self.color_theme_torque)
        HACKER = COLOR_THEME.addAction("HACKER")
        HACKER.triggered.connect(self.color_theme_hacker)

        # help
        HELP = mainMenu.addMenu("HELP")
        ABOUT = HELP.addAction("ABOUT")
        ABOUT.triggered.connect(self.msg)
        DEVELOPERS = HELP.addAction("DEVELOPERS")
        DEVELOPERS.triggered.connect(self.msg2)

        self.default_format()  # Call default formatting method after setting up the UI
        
        self.show()
        # self.close()

    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label.setFont(QFont("Verdana 7"))
        self.sent_label.move(0, 583)
        self.sent_label.resize(496, 40)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.sent_label.setFont(font)
        # self.sent_label.setStyleSheet("QLabel{background-color:#EEEEEE;color:#000000}")
        self.sent_label.setText(date)
        print(date)

    # def send_message_insert(self):

    #     user_input = self.textEdit.toPlainText()

    #     self.textEdit.clear()
    #     pr1 = "Human : " + user_input + "\n"
    #     # pr1 = ("Human: " + user_input + "\n").setAlignment(Qt.AlignRight)
    #     ob = chat(user_input)
    #     pr = "COBOT : " + ob + "\n" + "\n"
    #     # self.con = self.con + pr1.setAlignment(Qt.AlignRight) + pr.setAlignment(Qt.AlignLeft)
    #     self.con = self.con + pr1 + pr
    #     self.textBrowser.setEnabled(True)
    #     self.textBrowser.setText(self.con)
    #     self.last_sent_label(str(time.strftime("Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
    #     self.textEdit.clear()
    #     time.sleep(0)
    #     t2 = threading.Thread(target=self.playResponce, args=(ob,))
    #     t2.start()
        
    def send_message_insert(self):
     user_input = self.textEdit.toPlainText()
     self.textEdit.clear()

     # Define HTML icon code for user and bot
     user_icon_html = '<span class="user-icon">👤</span>'
     bot_icon_html = '<span class="bot-icon">\U0001F916</span>'

     # Format user question and bot response with HTML and include icons
     pr1 = f'<div class="user-message" style="text-align: left;">{user_icon_html} : {user_input}</div>'
     ob = chat(user_input)
     pr = f'<br/><div class="bot-message" style="text-align: right;">{bot_icon_html} : {ob}</div><br>'

     # Append formatted messages to the QTextBrowser
     self.con += pr1 + pr

     # Update the QTextBrowser with the formatted messages
     self.textBrowser.setEnabled(True)
     self.textBrowser.setText(self.con)

     # Update the last sent label
     self.last_sent_label(str(time.strftime("Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))

     # Clear the text edit
     self.textEdit.clear()

     # Start a thread to play the response
     t2 = threading.Thread(target=self.playResponce, args=(ob,))
     t2.start()





        
    




    def playResponce(self, responce):
       subprocess.call(["say","-v","Samantha",responce])

    # played successfully
    def clear_chat(self):
        self.con = ""
        self.textBrowser.setText("")
        self.textBrowser.setDisabled(True)
        # print("No messages sent")
        self.last_sent_label(date="No messages sent.")

    def chatexit(self):
        self.closeEvent2(self)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self, "WARNING", "Are you sure you want to exit COBOT?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.No:
            event.ignore()

        else:
            # event.accept()
            self.close()

    def closeEvent2(self, event):
        close = QtWidgets.QMessageBox.question(self, "WARNING", "Are you sure you want to exit COBOT?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.No:
            pass
        else:
            # exit()
            self.destroy()

    def font_change_default(self):
        self.textBrowser.setFont(QFont("Verdana 10"))
        self.textEdit.setFont(QFont("Verdana 10"))
        self.font = "Verdana"

    def font_change_times(self):
        self.textBrowser.setFont(QFont("Times"))
        self.textEdit.setFont(QFont("Times"))
        self.font = "Times"

    def font_change_system(self):
        self.textBrowser.setFont(QFont("System"))
        self.textEdit.setFont(QFont("System"))
        self.font = "System"

    def font_change_helvetica(self):
        self.textBrowser.setFont(QFont("helvetica 10"))
        self.textEdit.setFont(QFont("helvetica 10"))
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.textBrowser.setFont(QFont("fixedsys"))
        self.textEdit.setFont(QFont("fixedsys"))
        self.font = "fixedsys"

    def color_theme_default(self):
        self.setStyleSheet("background-color:#EEEEEE")
        self.textBrowser.setStyleSheet("background-color:#FFFFFF,color:#000000")
        self.textEdit.setStyleSheet("QTextEdit{background-color:#FFFFFF,color:#000000}")
        self.pushButton.setStyleSheet("background-color:#FFFFFF, fcolor:#000000")
        self.sent_label.setStyleSheet("background-color:#EEEEEE, color:=#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

        # Dark

    def color_theme_dark(self):
        self.setStyleSheet("background-color: #2a2b2d;color:#FFFFFF;")
        self.textBrowser.setStyleSheet("background-color: #212121;color:#FFFFFF;")
        self.textEdit.setStyleSheet("QTextEdit { background-color : #212121; color : #FFFFFF; }")
        self.pushButton.setStyleSheet("QPushButton{background-color:#212121; color:#FFFFFF}")
        self.sent_label.setStyleSheet("background-color:#2a2b2d, color:#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

        # Grey

    def color_theme_grey(self):
        self.setStyleSheet("background-color:#444444;color:#ffffff")
        self.textBrowser.setStyleSheet("background-color: #4f4f4f;color:#ffffff;")
        self.textEdit.setStyleSheet("QTextEdit { background-color : #4f4f4f; color : #ffffff; }")
        self.pushButton.setStyleSheet("QPushButton{background-color:#4f4f4f; color:#ffffff}")
        self.sent_label.setStyleSheet("background-color:#444444, color:#ffffff")
        #
        self.tl_bg = "#212121"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"
        #

    def color_theme_torque(self):
        self.setStyleSheet("background-color:#003333;color:#FFFFFF")
        self.textBrowser.setStyleSheet("background-color: #669999;color:#FFFFFF;")
        self.textEdit.setStyleSheet("QTextEdit { background-color : #669999; color : #FFFFFF; }")
        self.pushButton.setStyleSheet("QPushButton{background-color:#669999; color:#FFFFFF}")
        self.sent_label.setStyleSheet("background-color:#003333, color:#FFFFFF")
        #
        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

        # Blue

    def color_theme_blue(self):
        self.setStyleSheet("background-color:#263b54;color:#FFFFFF")
        self.textBrowser.setStyleSheet("background-color: #1c2e44;color:#FFFFFF;")
        self.textEdit.setStyleSheet("QTextEdit { background-color : #1c2e44; color : #FFFFFF; }")
        self.pushButton.setStyleSheet("QPushButton{background-color:#1c2e44;color:#FFFFFF}")
        self.sent_label.setStyleSheet("background-color:#263b54, color:=#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

        # Hacker

    def color_theme_hacker(self):
        self.setStyleSheet("background-color:#0F0F0F;color:#33FF33")
        self.textBrowser.setStyleSheet("background-color:#0F0F0F; color:#33FF33")
        self.textEdit.setStyleSheet("QTextEdit { background-color :#0F0F0F ; color : #33FF33; }")
        self.pushButton.setStyleSheet("QPushButton{background-color:#0F0F0F; color:#33FF33}")
        self.sent_label.setStyleSheet("background-color=#0F0F0F, color:#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    def msg(self):
        self.msg_box = QMessageBox()
        self.msg_box.setGeometry(1420, 600, width, height)
        # self.setGeometry(1420, 400, width, height)

        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("COBOT v1.0")
        self.msg_box.setText(
            'COBOT is a chatbot for answering COVID related queries\nIt is based on retrival-based NLP using pythons NLTK tool-kit module\nGUI is based on PyQt5\nIt can answer questions regarding the pandemic at present times')
        self.msg_box.show()

    def msg2(self):
        self.msg_box = QMessageBox()
        self.msg_box.setGeometry(1580, 600, width, height)
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setWindowTitle("DEVELOPERS")
        self.msg_box.setText('1.RIYA SAHU \n2.SEJAL AGRAWAL \n 3.SUYASH KHARE \n 4.YASHI AGARWAL')
        
        # Center the message box on the screen
        msg_box_geometry = self.msg_box.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        msg_box_geometry.moveCenter(center_point)
        self.msg_box.move(msg_box_geometry.topLeft())
        self.msg_box.show()

    def default_format(self):
        self.color_theme_default()
        self.font_change_default()
        self.color_theme_torque()


# app = QApplication(sys.argv)

# GUI = ChatInterface()
# sys.exit(app.exec_())
