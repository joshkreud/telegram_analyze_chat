import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot(ser: pd.Series):
    ax = plt.subplot(111, polar=True)
    equals = np.linspace(0, 360, 24, endpoint=False)  # np.arange(24)
    ones = ser
    ax.bar(equals, ones)

    # Set the circumference labels
    ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
    ax.set_xticklabels(range(24))

    # Make the labels go clockwise
    ax.set_theta_direction(-1)

    # Place 0 at the top
    ax.set_theta_offset(np.pi / 2.0)

    plt.show()