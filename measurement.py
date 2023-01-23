from datetime import datetime


class Measurement:
    """Class Measurement models sugar in blood measurement

    :param sugar: amount of sugar in the blood mg/dl
    :param date: date and hour of measurement
    :param mode: was the measurement after meal or not
     """

    sugar: int
    date: datetime
    mode: str

    def __init__(self, sugar, date, mode):
        """
        :param sugar: amount of sugar in the blood mg/dl
        :type int
        :param date: date and hour of measurement
        :type datetime
        :param mode: was the measurement after meal or not
        :type: str
        """
        self.sugar = sugar
        self.date = date
        self.mode = mode

    def __str__(self):
        """Returns formatted string that is a description of measurement

        :return: formatted string that is a description of measurement
        :type: str
        """
        formatted_date = self.date.strftime('%d.%m.%Y %H:%M')
        return f'{str(round(self.sugar))} {formatted_date} {self.mode}'
