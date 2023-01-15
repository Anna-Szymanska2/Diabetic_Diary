
from measurements_database import *
from firstPage import FirstPage
from secondPage import SecondPage


class Controller:
    def __init__(self):
        self.database = MeasurementsDataBase()
        self.first_page = FirstPage(self)
        self.second_page = SecondPage(self)

    def string_measurement_list(self):
        measurements_list = self.database.measurements_list.copy()
        string_list = []
        for i in measurements_list:
            string_list.append(i.__str__())
        return string_list



