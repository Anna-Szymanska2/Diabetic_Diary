import sqlite3
from measurement import Measurement
from datetime import datetime
from operator import attrgetter
from statistics import mean
from dateutil.relativedelta import relativedelta


def analise_measurements(measurements_list):
    measurements_list_copy = measurements_list.copy()
    measurements_list_copy.sort(key=attrgetter('sugar'))
    sugar_list = []
    [sugar_list.append(measurement.sugar) for measurement in measurements_list_copy]
    average_sugar = mean(sugar_list)
    min_sugar = sugar_list[0]
    max_sugar = sugar_list[-1]
    return average_sugar, min_sugar, max_sugar


class MeasurementsDataBase:

    def __init__(self):
        self.conn = sqlite3.connect('pomiary.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS pomiary
                          (sugar REAL,
                           measurement_date TEXT)''')
        self.c.execute('SELECT * FROM pomiary')
        self.measurements_list = []
        for row in self.c.fetchall():
            sugar, measurement_date = row
            measurement_date = datetime.strptime(measurement_date, '%d.%m.%Y %H:%M')
            self.measurements_list.append(Measurement(sugar, measurement_date))

    def find_measurements_from_period(self, period, start_date):
        match period:
            case 1:
                #end_date = start_date.replace(year=start_date.year + 1)
                end_date = start_date + relativedelta(years=+1)
                print(end_date)
            case 2:
                end_date = start_date + relativedelta(months=+1)
                print(end_date)
            case 3:
                end_date = start_date + relativedelta(days=+7)
                print(end_date)
            case 4:
                end_date = start_date + relativedelta(days=+1)
                print(end_date)

    def display_all_measurements(self):
        """A function that displays all results stored in the database"""
        print()
        print("Twoje wszystkie zapisane pomiary:")
        print()
        self.c.execute('SELECT * FROM pomiary ORDER BY measurement_date')
        print("Cukier Data pomiaru")
        for row in self.c.fetchall():
            sugar, measurement_date = row
            print(str(sugar) + " " * (len("Cukier ") - len(str(sugar))) +
                  str(measurement_date) + " " * (len("Data pomiaru ") - len(str(measurement_date))))

        [print(i, end='\n') for i in self.measurements_list]

    def add_new_measurement(self, sugar, date):
        sugar = int(sugar)
        measurement_date = datetime.strptime(date, '%d.%m.%Y %H:%M')
        current_date = datetime.now()
        if measurement_date > current_date:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("Data nie może być przyszła")
            return
        if sugar > 200 or sugar < 10:
            print("Podana przez Ciebie wartość nie jest możliwa, podany cukier musi mieścić się w przedziale <10,200>")
            return
        if sugar > 140:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("To zbyt wysoki wynik, możesz mieć cukrzycę")
        if sugar < 70:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("To zbyt niski wynik, możesz mieć cukrzycę")

        measurement = Measurement(sugar, measurement_date)
        if any(x.date == measurement_date for x in self.measurements_list):
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("W bazie danych istnieje już pomiar z taką datą, więc nie można go dodać")
            return
        self.measurements_list.append(measurement)
        script = """INSERT INTO pomiary VALUES (?, ?)"""
        self.conn.execute(script, (sugar, date))
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
        """A function that deletes all the measurements from the database.

        It also asks user if he is sure that he wants to do this before clearing all saved data
        """

        self.c.execute('DELETE FROM pomiary')
        self.conn.commit()
        self.measurements_list.clear()
        print('Baza danych została wyczyszczona')




