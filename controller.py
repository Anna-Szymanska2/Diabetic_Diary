from datetime import datetime

import measurements_database
from measurements_database import *
from histogram import *


class Controller:
    def __init__(self):
        self.database = MeasurementsDataBase()

    def string_measurement_list(self):
        measurements_list = self.database.measurements_list.copy()
        string_list = []
        for i in measurements_list:
            string_list.append(i.__str__())
        return string_list



