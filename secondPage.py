from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QDateTimeEdit, QPushButton, QListWidget, QHBoxLayout, \
    QGridLayout, QVBoxLayout


class SecondPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        measurements_list = controller.database.measurements_list.copy()

        time_period_label = QLabel("Zakres czasu: ")
        self.combo_box_time = QComboBox(self)
        self.combo_box_time.addItem("Rok")
        self.combo_box_time.addItem("Miesiąc")
        self.combo_box_time.addItem("Tydzień")
        self.combo_box_time.addItem("Dzień")

        start_time_label = QLabel("Czas rozpoczęcia: ")
        dateEdit = QDateTimeEdit(QDateTime.currentDateTime())

        mode_label = QLabel("Rodzaj pomiarów: ")
        self.combo_box_mode = QComboBox(self)
        self.combo_box_mode.addItem("Wyszystkie")
        self.combo_box_mode.addItem("Na czczo")
        self.combo_box_mode.addItem("Po jedzeniu")

        button_analise = QPushButton("Analiza")

        self.list_widget = QListWidget(self)
        measurements_list = controller.database.measurements_list.copy()
        string_list = []
        for i in measurements_list:
            string_list.append(" " * (len("Cukier ") - len(str(i.sugar))) + str(i.sugar) +
                               " " * (len("Data wykonania pomiaru ") - len(str(i.date))) +
                               str(i.date) + " " * (len("Tryb pomiaru ") - len(str(i.mode))) + str(i.mode))

        self.list_widget.addItems(string_list)

        avg_label = QLabel("Cukier średni: ")
        min_label = QLabel("Cukier min: ")
        max_label = QLabel("Cukier max: ")

        v_layout_labels = QVBoxLayout()
        v_layout_labels.addWidget(avg_label)
        v_layout_labels.addWidget(min_label)
        v_layout_labels.addWidget(max_label)

        image_label = QLabel()

        h_layout = QHBoxLayout()
        h_layout.addWidget(time_period_label)
        h_layout.addWidget(self.combo_box_time)
        h_layout.addWidget(start_time_label)
        h_layout.addWidget(dateEdit)
        h_layout.addWidget(mode_label)
        h_layout.addWidget(self.combo_box_mode)
        h_layout.addWidget(button_analise)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.list_widget, 0, 0)
        grid_layout.addLayout(v_layout_labels, 1, 0)
        grid_layout.addWidget(image_label, 1, 0, 2, 2)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addLayout(grid_layout)

        self.setLayout(v_layout)

