import sqlite3
from measurement import Measurement
from datetime import datetime
from operator import attrgetter
from statistics import mean
from dateutil.relativedelta import relativedelta

"""Module measurement_database gives tools to work with database of sugar measurements"""


def string_measurement_list(measurements_list):
    string_list = []
    for i in measurements_list:
        string_list.append(i.__str__())
    return string_list


def return_sugar_values(measurements_list):
    """Creates list of sugars values taken from measurements from the list of them

    :param measurements_list: list of measurements
    :type: list
    :return: list of sugars values
    :type: list
    """

    sugar_list = []
    [sugar_list.append(measurement.sugar) for measurement in measurements_list]
    return sugar_list


def analise_measurements(measurements_list):
    """Returns statistic properties of measurements on the list

    :param measurements_list: list of measurements
    :return: statistic properties of measurements (average, min, max)
    :Tuple
    """

    measurements_list_copy = measurements_list.copy()
    measurements_list_copy.sort(key=attrgetter('sugar'))
    sugar_list = return_sugar_values(measurements_list_copy)
    average_sugar = mean(sugar_list)
    average_sugar = round(average_sugar, 1)
    min_sugar = sugar_list[0]
    max_sugar = sugar_list[-1]
    return average_sugar, min_sugar, max_sugar


def find_measurements_with_specific_mode(mode, measurements_list):
    """Returns list of measurements with specific mode (after the meal or not)

    :param mode: says whether measurement was taken after the meal or not
    :type: str
    :param measurements_list: list of measurement from which we add measurements that match
    :return: list of measurements with specific mode
    :type: list
    """

    measurements_with_specific_mode = []
    for measurement in measurements_list:
        if measurement.mode == mode:
            measurements_with_specific_mode.append(measurement)

    return measurements_with_specific_mode


def return_start_date(period, end_date):
    """Returns date that is before the taken date from chosen distance.

    :param period: chosen distance
    :type: int
    :param end_date: the date from which we count
    :type: datetime
    :return: the date that is before the taken date
    :type: datetime
    """

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
    """Returns list that has measurements with date that is between two dates.

    :param period: how long is the distance between two dates
    :param end_date: the later date
    :type: datetime
    :param measurements_list: list of measurements
    :type: list
    :return: measurements from period
    :type: list
    """

    start_date = return_start_date(period, end_date)
    end_date = datetime.strptime(end_date, '%d.%m.%Y %H:%M')
    measurements_from_period = []
    for measurement in measurements_list:
        if start_date < measurement.date <= end_date:
            measurements_from_period.append(measurement)

    return measurements_from_period


def return_sorted_chronologically(measurements_list):
    """Returns list that is a copy of argument list sorted chronologically.

    :param measurements_list: list of measurements
    :type: list
    :return: list sorted chronologically
    :type: list
    """

    measurements_list = measurements_list.copy()
    measurements_list.sort(key=attrgetter('date'))
    return measurements_list


class MeasurementsDataBase:
    """Class Measurement models sugar in blood measurement

    :param conn: connection with sqlite3 database
    :param c: cursor from sqlite3
    :param measurements_list: list of all measurements from database
    """

    def __init__(self):
        """

        :param conn: connection with sqlite3 database
        :type Connection
        :param c: cursor from sqlite3
        :type Cursor
        :param measurements_list: list of all measurements from database
        :type: list
        """
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
        """Adds new measurement to the list of them and to the database if they are correct (checks it before).

        :param sugar: amount of sugar in the blood mg/dl
        :type int
        :param date: date and hour of measurement
        :type datetime
        :param mode: was the measurement after meal or not
        :type: str
        :return: information about adding or not adding measurement
        :type: str
        """

        sugar = int(sugar)
        measurement_date = datetime.strptime(date, '%d.%m.%Y %H:%M')
        current_date = datetime.now()
        s = " "
        if measurement_date > current_date:
            return "Date cannot be from future"
        if sugar > 400 or sugar < 10:
            return "Such value is impossible, try something from range <10,400>"
        if mode == "after eating":
            if sugar > 140:
               s = "Value is too high, you can suffer from diabetes"
        else:
            if sugar > 100:
                s = "Value is too high, you can suffer from diabetes"
        if sugar < 70:
            s = "Value is too low, you can suffer from diabetes"

        measurement = Measurement(sugar, measurement_date, mode)
        if any(x.date == measurement_date for x in self.measurements_list):
            return "There is measurement in database with such date so you cannot add it"
        self.measurements_list.append(measurement)
        script = """INSERT INTO pomiary VALUES (?, ?, ?)"""
        self.conn.execute(script, (sugar, date, mode))
        self.conn.commit()
        return s + "\n"+"Adding to database was successful"

    def clear_all_measurements(self):
        """Deletes all the measurements from the database and the list.

        :return: information about deleting
        :type: str
        """

        self.c.execute('DELETE FROM pomiary')
        self.conn.commit()
        self.measurements_list.clear()

        return "Database was cleared"

    def delete_measurement_at_date(self, date):
        """Deletes chosen by the user measurement"""

        for measurement in self.measurements_list:
            if measurement.date == date:
                measurement_to_remove = measurement
        self.measurements_list.remove(measurement_to_remove)
        date = date.strftime('%d.%m.%Y %H:%M')
        self.c.execute(f'DELETE FROM pomiary WHERE measurement_date="{date}";')
        self.conn.commit()



