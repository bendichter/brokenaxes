"""
Different scales with brokenaxes
================================

This example shows how to customize the scales and the ticks of each broken
axes.
"""

import numpy as np
from brokenaxes import brokenaxes
import matplotlib.ticker as ticker

x = np.linspace(0, 5*2*np.pi, 300)
y1 = np.sin(x)*100
y2 = np.sin(x+np.pi)*5 + 90
y3 = 30*np.exp(-x) - 50
y4 = 90 + (1-np.exp(6/x))

bax = brokenaxes(
    ylims=[(-100, 0), (80, 100)],
    xlims=[(0, 5), (10, 30)],
    height_ratios=[1, 3],
    width_ratios=[3, 5]
)

bax.plot(x, y1, label="Big sin")
bax.plot(x, y2, label="Small sin")
bax.plot(x, y3, label="Exponential 1")
bax.plot(x, y4, '--', label="Exponential 2")

bax.legend(loc="lower right")
bax.set_title("Example for different scales for the x and y axis")

# Then, we get the different axes created and set the ticks according to the
# axe x and y limits.
# Since it is normal matplotlib axes, you could also set them manually, for
# instance with `bax.axs[2].set_yticks([-100, -50, 0])`.

for i, ax in enumerate(bax.last_row):
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.set_xlabel('xscale {i}'.format(i=i))
for i, ax in enumerate(bax.first_col):
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.set_ylabel('yscale {i}'.format(i=i))

# Note: it is not necessary to loop through all the axes since they all share
# the same x and y limits in a given column or row.
