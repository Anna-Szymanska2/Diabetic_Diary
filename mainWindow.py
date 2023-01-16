from PySide6.QtWidgets import QMainWindow, QStackedWidget
from measurements_database import *
from firstPage import FirstPage
from secondPage import SecondPage


class MainWindow(QMainWindow):
    """ Class MainWindow is used to model main window of the application"""

    def __init__(self):
        super().__init__()
        self.database = MeasurementsDataBase()
        self.first_page = FirstPage(self.database)
        self.second_page = SecondPage(self.database)
        self.setWindowTitle("Dzienniczek diabetyka")
        menu_bar = self.menuBar()
        measurements = menu_bar.addAction("Pomiary")
        measurements.triggered.connect(self.measurements_action)
        analise = menu_bar.addAction("Analiza")
        analise.triggered.connect(self.analise_action)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.addWidget(self.first_page)

    def measurements_action(self):
        """Switches to first page view after clicking button"""

        first_page = self.first_page
        self.central_widget.addWidget(first_page)
        self.central_widget.setCurrentWidget(first_page)

    def analise_action(self):
        """Switches to second page view after clicking button"""

        second_page = self.second_page
        self.central_widget.addWidget(second_page)
        string_list = string_measurement_list(return_sorted_chronologically(self.database.measurements_list.copy()))
        second_page.list_widget.clear()
        second_page.list_widget.addItems(string_list)
        self.central_widget.setCurrentWidget(second_page)
