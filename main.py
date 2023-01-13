from datetime import datetime
import sqlite3
import math
from controller import Controller
from PySide6.QtWidgets import QApplication

from firstPage import FirstPage
from mainWindow import MainWindow
import sys

def main():
    #controller = Controller()
    #controller.main()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
