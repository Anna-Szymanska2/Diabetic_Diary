
from PySide6.QtWidgets import QMainWindow, QWidget, QSizePolicy

from controller import Controller
from firstPage import FirstPage
from secondPage import SecondPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dzienniczek diabetyka")
        controller = Controller()

        menu_bar = self.menuBar()
        menu_bar.addMenu("Pomiary")
        menu_bar.addMenu("Analiza")

        firstPage = FirstPage(controller)
        secondPage = SecondPage(controller)
        self.setCentralWidget(secondPage)
