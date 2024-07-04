import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QHeaderView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sqlite3 as lite
import sys

from PyQt5.uic.properties import QtWidgets

con = lite.connect('database.db')



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Ratings and reviews'
        self.left = 650
        self.top = 330
        self.width = 369
        self.height = 390

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedWidth(self.width)
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table

        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Name','Rating','Suggestions'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        with con:
            self.cur= con.cursor()
            self.cur.execute("SELECT * FROM Users")

            rows = self.cur.fetchall()

            for row in rows:
                inx = rows.index(row)
                self.tableWidget.insertRow(inx)
                # add more if there is more columns in the database.
                self.tableWidget.setItem(inx, 0, QTableWidgetItem(row[1]))
                self.tableWidget.setItem(inx, 1, QTableWidgetItem(row[2]))
                self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))
                #self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))
                #print(row)


        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
