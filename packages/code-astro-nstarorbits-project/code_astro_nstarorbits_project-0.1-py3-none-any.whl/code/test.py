import numpy as np
import matplotlib.pyplot as plt


def test_func(x,y):
    '''plot x versus y
    arguments:
	x (int, float, or array) : x value to be plotted
	y (int, flot, or array) : y value to be plotted
    returns: plot

    '''

    plt.plot(x,y)
    plt.show()
