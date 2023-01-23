import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.axis import Axis


def plot_histogram(sugar_values, border_value, mode, start_date, end_date):
    """Plots histogram of sugar values, good results are green, very bad red and bad are orange.

    :param sugar_values: values of sugar
    :type list
    :param border_value: border value that says which values should be orange
    :type int
    :param mode: says whether measurement was after meal
    :type int
    :param start_date: the first date of range from which measurements where taken
    :type str
    :param end_date: the last date of range from which measurements where taken
    :type str
    """
    bins = []
    i = 10
    while i <= 400:
        bins.append(i)
        i += 10
    fig = plt.figure()
    n, bin1, patches = plt.hist(sugar_values, bins=bins, color="green", ec="black")
    for i in range(4):
        patches[i].set_fc("red")
    patches[4].set_fc("orange")
    patches[5].set_fc("orange")
    for i in range(19, 39):
        patches[i].set_fc("red")
    for i in range(int(border_value/10)-1, 19):
        patches[i].set_fc("orange")
    plt.xlabel("Cukier mg/dl")
    plt.ylabel("Częstość")
    plt.legend([patches[0], patches[4], patches[6]], ["zagrożenie życia", "nieprawidłowy cukier", "prawidłowy cukier"])
    fig.canvas.draw()
    fig.canvas.flush_events()
    if mode == 2:
        mode = "na czczo"
    else:
        mode = "po jedzeniu"
    end_date = end_date[:-6]
    plt.title(f"Histogram pomiarów cukru {mode}, okres {start_date} - {end_date}")
    plt.savefig('plot.png')
