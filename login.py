import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QTabWidget, QTextEdit
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPalette, QColor, QBrush
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QTextCharFormat

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        


        # Center the window on the screen
        screen_geometry = QApplication.desktop().screenGeometry()
        center_point = screen_geometry.center()
        self.move(center_point.x() - self.width() // 2, center_point.y() - self.height() // 2)


        # set the title of main window
        self.setWindowTitle('Sidebar layout')

        # Set the initial position of the window
        self.move(100, 10)

        # set the size of window
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('Home', self)
        self.btn_2 = QPushButton('About', self)
        self.btn_3 = QPushButton('Blogs', self)
        self.btn_4 = QPushButton('License', self)

        # Styling the buttons
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                border: 2px solid #4CAF50;
                font-size: 16px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
                border: 2px solid #3e8e41;
            }
        """)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Set sidebar background color to black
        left_widget.setStyleSheet("background-color: black;")

    # -----------------
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    # -----------------
    # pages

    def ui1(self):
     main_layout = QVBoxLayout()

     # Create a QLabel for the message
     message_label = QLabel()
     message_label.setText("Welcome to Covid Tracker")
     message_label.setStyleSheet("color: white; font-size: 20px; padding: 10px;")
     main_layout.addWidget(message_label)

     # Create a QTextEdit widget
     self.texting = QTextEdit()

     self.texting.setReadOnly(True)

     # Set background image for QTextEdit using palette
     background_pixmap = QPixmap('c.jpg').scaled(1200, 1200)  # Adjust the size as needed
     palette = self.texting.palette()
     palette.setBrush(QPalette.Base, QBrush(background_pixmap))
     self.texting.setPalette(palette)

     self.texting.setStyleSheet("QTextEdit {font-size: 44px; color: red;}")  # Set additional style properties
     self.texting.setFixedHeight(650)  # Set a fixed height (adjust as needed)
     self.texting.setFixedWidth(1000)
     self.texting.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scroll bar

     main_layout.addWidget(self.texting)

     # Adding clock
     self.clock_label = QLabel()
     main_layout.addWidget(self.clock_label) 

     main_layout.addStretch(5)
     main = QWidget()
     main.setLayout(main_layout)

     # Starting a timer
     self.timer = QTimer(self)
     self.timer.timeout.connect(self.update_clock)
     self.timer.start(1000)
     self.update_clock()
     return main
    
    def update_clock(self):
        # Calculate the elapsed time since COVID-19 arrival
        covid_start_date = QDateTime.fromString("2019-12-31T00:00:00", Qt.ISODate)  # Assuming COVID-19 started on Dec 31, 2019
        current_date = QDateTime.currentDateTime()
        elapsed_seconds = covid_start_date.secsTo(current_date)

        # Calculate days, hours, minutes, and seconds
        days = elapsed_seconds // (24 * 3600)
        hours = (elapsed_seconds % (24 * 3600)) // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60

        # Update the clock label text
        #self.clock_label.setText(f"Elapsed time since COVID-19: {days} days : {hours} hours : {minutes} minutes : {seconds} seconds")
        # Update the text of the QTextEdit widget
        message = f"\n \n \n \t \t \t Welcome to Covid Tracker\n \n \n\t \t \t Elapsed time since COVID-19:\n \t \t \t Days : hours : minutes : seconds \n \t \t \t {days} : \t {hours} \t : \t{minutes} \t   : \t {seconds}</font>"

        self.texting.setPlainText(message)
        self.texting.setStyleSheet("color: green;")  # Change text color to green



    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('About'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('Blogs'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('License'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
