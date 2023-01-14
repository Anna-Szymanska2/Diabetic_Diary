from PySide6.QtWidgets import QMainWindow, QWidget, QSizePolicy, QStackedWidget

from controller import Controller
from firstPage import FirstPage
from secondPage import SecondPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        first_page = FirstPage(self.controller)

        self.setWindowTitle("Dzienniczek diabetyka")

        menu_bar = self.menuBar()
        measurements = menu_bar.addAction("Pomiary")
        measurements.triggered.connect(self.measurements_action)
        analise = menu_bar.addAction("Analiza")
        analise.triggered.connect(self.analise_action)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.addWidget(first_page)

    def measurements_action(self):
        first_page = FirstPage(self.controller)
        self.central_widget.addWidget(first_page)
        self.central_widget.setCurrentWidget(first_page)

    def analise_action(self):
        second_page = SecondPage(self.controller)
        self.central_widget.addWidget(second_page)
        self.central_widget.setCurrentWidget(second_page)
