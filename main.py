from datetime import datetime
import sqlite3
import math
from controller import Controller
from PySide6.QtWidgets import QApplication

from firstPage import FirstPage
from mainWindow import MainWindow
import sys

"""Diary for sugar in blood measurements 

This script allows user to gather their sugar measurements in a database. Application has graphic user interface. 
The user has possibility of adding new measurement, deleting the chosen one, displaying all collected measurements 
and analysing their statistical properties. The app enables to draw histogram of measurements from chosen timeline.
"""

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
