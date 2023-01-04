import matplotlib.pyplot as plt


def plot_histogram(sugar_values):
    plt.hist(sugar_values, bins=10)
    plt.show()