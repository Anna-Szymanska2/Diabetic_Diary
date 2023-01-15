import sqlite3
from measurement import Measurement
from datetime import datetime
from operator import attrgetter
from statistics import mean
from dateutil.relativedelta import relativedelta


def return_sugar_values(measurements_list):
    sugar_list = []
    [sugar_list.append(measurement.sugar) for measurement in measurements_list]
    return sugar_list


def analise_measurements(measurements_list):
    measurements_list_copy = measurements_list.copy()
    measurements_list_copy.sort(key=attrgetter('sugar'))
    sugar_list = return_sugar_values(measurements_list_copy)
    average_sugar = mean(sugar_list)
    average_sugar = round(average_sugar, 1)
    min_sugar = sugar_list[0]
    max_sugar = sugar_list[-1]
    return average_sugar, min_sugar, max_sugar


def find_measurements_with_specific_mode(mode, measurements_list):
    measurements_with_specific_mode = []
    for measurement in measurements_list:
        if measurement.mode == mode:
            measurements_with_specific_mode.append(measurement)

    return measurements_with_specific_mode


def return_start_date(period, end_date):
    end_date = datetime.strptime(end_date, '%d.%m.%Y %H:%M')
    match period:
        case 1:
            start_date = end_date + relativedelta(years=-1)
        case 2:
            start_date = end_date + relativedelta(months=-1)
        case 3:
            start_date = end_date + relativedelta(days=-7)
        case 4:
            start_date = end_date + relativedelta(days=-1)
    return start_date


def find_measurements_from_period(period, end_date, measurements_list):

    start_date = return_start_date(period, end_date)
    end_date = datetime.strptime(end_date, '%d.%m.%Y %H:%M')
    measurements_from_period = []
    for measurement in measurements_list:
        if start_date < measurement.date <= end_date:
            measurements_from_period.append(measurement)

    return measurements_from_period


def return_sorted_chronologically(measurements_list):
    measurements_list = measurements_list.copy()
    measurements_list.sort(key=attrgetter('date'))
    return measurements_list


class MeasurementsDataBase:

    def __init__(self):
        self.conn = sqlite3.connect('pomiary.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS pomiary
                          (sugar REAL, measurement_date TEXT, mode TEXT)''')
        self.c.execute('SELECT * FROM pomiary')
        self.measurements_list = []
        for row in self.c.fetchall():
            sugar, measurement_date, mode = row
            measurement_date = datetime.strptime(measurement_date, '%d.%m.%Y %H:%M')
            self.measurements_list.append(Measurement(sugar, measurement_date, mode))

    def add_new_measurement(self, sugar, date, mode):
        sugar = int(sugar)
        measurement_date = datetime.strptime(date, '%d.%m.%Y %H:%M')
        current_date = datetime.now()
        s = " "
        if measurement_date > current_date:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            return "Data nie może być przyszła"
        if sugar > 400 or sugar < 10:
            return "Podana przez Ciebie wartość nie jest możliwa, podany cukier musi mieścić się w przedziale <10,400>"
        if mode == "po jedzeniu":
            if sugar > 140:
                # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
               s = "To zbyt wysoki wynik, możesz mieć cukrzycę"
        else:
            if sugar > 100:
                # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
                s = "To zbyt wysoki wynik, możesz mieć cukrzycę"
        if sugar < 70:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            s = "To zbyt niski wynik, możesz mieć cukrzycę"

        measurement = Measurement(sugar, measurement_date, mode)
        if any(x.date == measurement_date for x in self.measurements_list):
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            return "W bazie danych istnieje już pomiar z taką datą, więc nie można go dodać"
        self.measurements_list.append(measurement)
        script = """INSERT INTO pomiary VALUES (?, ?, ?)"""
        self.conn.execute(script, (sugar, date, mode))
        self.conn.commit()
        # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
        return s + "\n"+"Podane przez Ciebie dane zostały dodane do bazy"

    def clear_all_measurements(self):
        """A function that deletes all the measurements from the database and the list."""

        self.c.execute('DELETE FROM pomiary')
        self.conn.commit()
        self.measurements_list.clear()

        return "Baza danych została wyczyszczona"

    def delete_measurement_at_date(self, date):
        for measurement in self.measurements_list:
            if measurement.date == date:
                measurement_to_remove = measurement
        self.measurements_list.remove(measurement_to_remove)
        date = date.strftime('%d.%m.%Y %H:%M')
        self.c.execute(f'DELETE FROM pomiary WHERE measurement_date="{date}";')
        self.conn.commit()




