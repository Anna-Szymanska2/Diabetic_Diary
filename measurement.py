from datetime import datetime


class Measurement:

    def __init__(self, sugar, date, mode):
        self.sugar = sugar
        self.date = date
        self.mode = mode

    def __str__(self):
        formatted_date = self.date.strftime('%d.%m.%Y %H:%M')
        return f'{str(round(self.sugar))} {formatted_date} {self.mode}'
