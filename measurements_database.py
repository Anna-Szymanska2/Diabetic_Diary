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


def find_measurements_from_period(period, start_date, measurements_list):
    match period:
        case '1':
            end_date = start_date + relativedelta(years=+1)
        case '2':
            end_date = start_date + relativedelta(months=+1)
        case '3':
            end_date = start_date + relativedelta(days=+7)
        case '4':
            end_date = start_date + relativedelta(days=+1)

    measurements_from_period = []
    for measurement in measurements_list:
        if start_date <= measurement.date < end_date:
            measurements_from_period.append(measurement)

    return measurements_from_period


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

    def display_all_measurements(self):
        """A function that displays all results stored in the database"""
        print()
        print("Twoje wszystkie zapisane pomiary:")
        print()
        self.c.execute('SELECT * FROM pomiary ORDER BY measurement_date')
        print("Cukier Data pomiaru")
        for row in self.c.fetchall():
            sugar, measurement_date, _ = row
            print(str(sugar) + " " * (len("Cukier ") - len(str(sugar))) +
                  str(measurement_date) + " " * (len("Data pomiaru ") - len(str(measurement_date))))

        [print(i, end='\n') for i in self.measurements_list]

    def add_new_measurement(self, sugar, date, mode):
        sugar = int(sugar)
        measurement_date = datetime.strptime(date, '%d.%m.%Y %H:%M')
        current_date = datetime.now()
        if measurement_date > current_date:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("Data nie może być przyszła")
            return
        if sugar > 400 or sugar < 10:
            print("Podana przez Ciebie wartość nie jest możliwa, podany cukier musi mieścić się w przedziale <10,400>")
            return
        if mode == "po jedzeniu":
            if sugar > 140:
                # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
                print("To zbyt wysoki wynik, możesz mieć cukrzycę")
        else:
            if sugar > 100:
                # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
                print("To zbyt wysoki wynik, możesz mieć cukrzycę")
        if sugar < 70:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("To zbyt niski wynik, możesz mieć cukrzycę")

        measurement = Measurement(sugar, measurement_date, mode)
        if any(x.date == measurement_date for x in self.measurements_list):
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("W bazie danych istnieje już pomiar z taką datą, więc nie można go dodać")
            return
        self.measurements_list.append(measurement)
        script = """INSERT INTO pomiary VALUES (?, ?, ?)"""
        self.conn.execute(script, (sugar, date, mode))
        self.conn.commit()
        # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
        print("Podane przez Ciebie dane zostały dodane do bazy")

    def delete_last_measurement(self):
        """A function that deletes recently added measurement from the database"""
        self.c.execute('DELETE FROM pomiary WHERE rowid = (SELECT MAX(rowid) FROM pomiary)')
        self.conn.commit()
        self.measurements_list.pop(-1)
        print('Pomiar został usunięty')

    def clear_all_measurements(self):
        """A function that deletes all the measurements from the database."""

        self.c.execute('DELETE FROM pomiary')
        self.conn.commit()
        self.measurements_list.clear()
        print('Baza danych została wyczyszczona')




