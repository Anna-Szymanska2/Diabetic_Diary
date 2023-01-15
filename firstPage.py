import re

from PySide6.QtCore import QDate, QTime, QDateTime
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, \
    QDateTimeEdit, QHBoxLayout, QMessageBox

from datetime import datetime


class FirstPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.list_widget = QListWidget(self)
        string_list = self.controller.string_measurement_list()

        self.list_widget.addItems(string_list)

        sugar_label = QLabel("Poziom cukru: ")
        self.line_edit = QLineEdit()

        mode_label = QLabel("Tryb: ")
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Na czczo")
        self.combo_box.addItem("Po posiłku")

        self.dateEdit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dateEdit.setMaximumDate(QDate.currentDate())
        self.dateEdit.setMaximumTime(QTime.currentTime())
        self.dateEdit.setDisplayFormat("dd.MM.yyyy hh:mm")

        h_layout = QHBoxLayout()

        h_layout.addWidget(sugar_label)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(mode_label)
        h_layout.addWidget(self.combo_box)
        h_layout.addWidget(self.dateEdit)

        button_add_item = QPushButton("Dodaj pomiar")
        button_add_item.clicked.connect(self.add_item)

        button_delete_item = QPushButton("Usuń zaznaczony pomiar")
        button_delete_item.clicked.connect(self.delete_item)

        button_delete_all = QPushButton("Usuń wszystkie pomiary")
        button_delete_all.clicked.connect(self.delete_all_items)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(button_add_item)
        v_layout.addWidget(self.list_widget)
        v_layout.addWidget(button_delete_item)
        v_layout.addWidget(button_delete_all)

        self.setLayout(v_layout)

    def add_item(self):
        length = len(self.controller.string_measurement_list().copy())
        sugar = self.line_edit.text()
        date = self.dateEdit.dateTime().toString(self.dateEdit.displayFormat())
        mode = self.combo_box.currentIndex()

        if mode == 1:
            mode = "po jedzeniu"
        else:
            mode = "na czczo"
        try:
            s = self.controller.database.add_new_measurement(sugar, date, mode)
            if len(self.controller.string_measurement_list().copy()) > length:
                self.list_widget.clear()
                string_list = self.controller.string_measurement_list()
                self.list_widget.addItems(string_list)
            self.show_message_box(" ", s)
        except ValueError:
            self.show_message_box("Błąd", "Podałeś dane w nieodpowiednim formacie")

    def delete_all_items(self):
        ret = QMessageBox.question(self, "Message Title",
                                   "Czy jesteś pewnien, że chcesz usunąć wszytkie pomiary?",
                                   QMessageBox.Ok | QMessageBox.Cancel)
        if ret == QMessageBox.Ok:
            s = self.controller.database.clear_all_measurements()
            self.show_message_box(" ", s)
            self.list_widget.clear()

    def delete_item(self):
        s = self.list_widget.currentItem().text()
        date = re.search('\d{2}.\d{2}.\d{4} \d{2}:\d{2}', s)
        measurement_date = datetime.strptime(date.group(), '%d.%m.%Y %H:%M')
        self.controller.database.delete_measurement_at_date(measurement_date)
        self.list_widget.takeItem(self.list_widget.currentRow())

    def show_message_box(self, title, value):
        ret = QMessageBox.information(self, title, value)
