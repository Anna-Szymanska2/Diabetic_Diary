from PySide6.QtCore import QDate, QTime, QDateTime
from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, \
    QDateTimeEdit, QHBoxLayout




class FirstPage(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.list_widget = QListWidget(self)
        measurements_list = controller.database.measurements_list.copy()
        string_list = []
        for i in measurements_list:
            string_list.append(" " * (len("Cukier ") - len(str(i.sugar))) + str(i.sugar) +
                               " " * (len("Data wykonania pomiaru ") - len(str(i.date))) +
                               str(i.date) + " " * (len("Tryb pomiaru ") - len(str(i.mode))) + str(i.mode))

        self.list_widget.addItems(string_list)

        sugar_label = QLabel("Poziom cukru: ")
        line_edit = QLineEdit()

        mode_label = QLabel("Tryb: ")
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Na czczo")
        self.combo_box.addItem("Po posiłku")

        dateEdit = QDateTimeEdit(QDateTime.currentDateTime())
        dateEdit.setMaximumDate(QDate.currentDate())
        dateEdit.setMaximumTime(QTime.currentTime())

        h_layout = QHBoxLayout()

        h_layout.addWidget(sugar_label)
        h_layout.addWidget(line_edit)
        h_layout.addWidget(mode_label)
        h_layout.addWidget(self.combo_box)
        h_layout.addWidget(dateEdit)

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
        self.list_widget.addItem("New Item")

    def delete_all_items(self):
        print("Item count : ", self.list_widget.count())

    def delete_item(self):
        self.list_widget.takeItem(self.list_widget.currentRow())
