import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.axis import Axis

def plot_histogram(sugar_values, border_value, mode, start_date, end_date):
    bins = []
    i = 10
    while i <= 400:
        bins.append(i)
        i += 10
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
    #nie wiem czy chcemy w ogole cos takiego wiec na razie nie poprawiam
    if mode == 2:
        mode = "na czczo"
    else:
        mode = "po jedzeniu"
    end_date = end_date[:-6]
    plt.title(f"Histogram pomiarów cukru {mode}, okres {start_date} - {end_date}")
   # x = [*range(10, 400, 20)]
   # plt.xticks(x)
    #formatter = ticker.FormatStrFormatter('?%1.2f')
   # Axis.set_major_formatter(formatter)
    #plt.show()
    plt.savefig('plot.png')
