import matplotlib.pyplot as plt


def plot_histogram(sugar_values, border_value):
    bins = []
    i = 10
    while i <= 400:
        bins.append(i)
        i += 10
    n, bin1, patches = plt.hist(sugar_values, bins=bins, color="green", ec="red")
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
    legend_drawn_flag = True
    plt.legend(["blue", "orange", "red"], loc=0, frameon=legend_drawn_flag)
    plt.show()
