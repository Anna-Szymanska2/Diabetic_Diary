from datetime import datetime

import measurements_database
from measurements_database import *
from histogram import *


def to_string_measurement_list(measurements_list):
    string_list = []
    for i in measurements_list:
        for i in measurements_list:
            string_list.append(i.__str__())
    return string_list


class Controller:
    def __init__(self):
        self.database = MeasurementsDataBase()

    def main(self):
        self.greet_user()
        actions = {
            '1': self.add_new_measurement_console,
            '2': self.database.display_all_measurements,
            '3': self.analise_measurements,
            '4': self.database.delete_last_measurement,
            '5': self.database.clear_all_measurements,
        }
        while True:
            self.print_first_menu()
            inp = input("Twój wybór ")
            if inp != 'q':
                action = actions.get(inp, None)
                if action is not None:
                    action()
                else:
                    print("Podałeś zły znak")
            else:
                print("Dziękuję za użycie")
                self.database.conn.close()
                break

    def greet_user(self):
        print("Cześć, jestem programem, który ułatwi Ci gromadzenie wyników pomiarów cukru")

    def print_first_menu(self):
        print()
        print("Wciśnij odpowedni klawisz i potwierdź enterem, żeby wykonać dostępne akcje")
        print("1 - dodaj nowy pomiar")
        print("2 - wyświetl już dodane badania")
        print("3 - analiza statystyczna już dodanych badań")
        print("4 - usuń ostatni dodany pomiar")
        print("5 - wyczyść bazę danych")
        print("q - wyłącz program")

    def print_second_menu(self):
        print()
        print("Wciśnij odpowedni klawisz i potwierdź enterem, żeby wybrać przedział czasu, w ktrorym chesz dokonac analizy")
        print("1 - rok")
        print("2 - miesiąc")
        print("3 - tydzień")
        print("4 - dzień")

    def add_new_measurement_console(self):
        """Asks user about measurement details and adds it to database.

        The function asks the user for details of measurements. Checks whether blood pressure and pulse have possible value
        and if the date is not a future date or too far away from the current date. If measurement details don't fit then
        the user is asked for them again. If everything is OK new measurement is added to the database.
        """
        sugar_string = input("Podaj wartość zmierzonego cukru ")
        measurement_date_string = input("Podaj date i godzine wykonania pomiaru, uźyj formatu 01.03.2022 15:34 ")
        mode = input("Podaj czy pomiar był po jedzeniu czy na czczo, 1- po jedzieniu, 2- na czczo")
        if mode == '1':
            mode = "po jedzeniu"
        else:
            mode = "na czczo"
        try:
            self.database.add_new_measurement(sugar_string, measurement_date_string, mode)
        except ValueError:
            # tu zakładam ze wstawisz jakiegos dialog boxa czy cos
            print("Podałeś dane w nieodpowiednim formacie")

    def analise_measurements(self):
        """A function that enables choosing which parameter should be analysed.

        It also checks if there is enough data in the database to conduct the analysis
        """
        self.print_second_menu()
        chosen_period = input("Podaj wybrana wartosc ")
        measurement_date_string = input("Podaj startową date i godzine wykonania pomiaru, uźyj formatu 01.03.2022 15:34 ")
        #measurement_date = datetime.strptime(measurement_date_string, '%d.%m.%Y %H:%M')
        self.database.delete_measurement_at_date(measurement_date_string)
        # mode = input("Podaj jakie pomiary chcesz analizowac 1- po jedzieniu, 2- na czczo, 3 - wszystkie")
        # measurements_list = self.database.measurements_list.copy()
        # if mode != '3':
        #     if mode == '1':
        #         measurements_list = find_measurements_with_specific_mode("po jedzeniu", measurements_list)
        #         border_value = 140
        #     else:
        #         measurements_list = find_measurements_with_specific_mode("na czczo", measurements_list)
        #         border_value = 100
        # if len(measurements_list) == 0:
        #     print("Nie ma pomiarów o takich własnościach")
        #     return
        # measurements_list = find_measurements_from_period(chosen_period, measurement_date, measurements_list)
        # if len(measurements_list) == 0:
        #     print("Nie ma pomiarów o takich własnościach")
        #     return
        # average, min_sugar, max_sugar = measurements_database.analise_measurements(measurements_list)
        # measurements_list_sorted = return_sorted_chronologically(measurements_list)
        # [print(i, end='\n') for i in measurements_list]
        # print("")
        # [print(i, end='\n') for i in measurements_list_sorted]
        # print(f'average: {average}, min: {min_sugar}, max: {max_sugar}')
        # if mode != '3':
        #     plot_histogram(return_sugar_values(measurements_list), border_value)

    def string_measurement_list(self):
        measurements_list = self.database.measurements_list.copy()
        string_list = []
        for i in measurements_list:
            for i in measurements_list:
                string_list.append(i.__str__())
        return string_list



