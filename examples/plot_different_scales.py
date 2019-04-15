"""
Different scales with brokenaxes
================================

This example shows how to customize the scales and the ticks of each broken
axes.
"""

#############################################################################
# brokenaxes lets you choose the aspect ratio of each sub-axes thanks to the
# `height_ratios` and `width_ratios` to over-pass the default 1:1 scale for all
# axes. However, by default the ticks spacing are still identical for all axes.
# In this example, we present how to customize the ticks of your brokenaxes.

import numpy as np
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import matplotlib.ticker as ticker


def make_plot():
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

    return bax


#############################################################################
# Use the AutoLocator() ticker
# ----------------------------

plt.figure()
bax = make_plot()

# Then, we get the different axes created and set the ticks according to the
# axe x and y limits.

for i, ax in enumerate(bax.last_row):
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.set_xlabel('xscale {i}'.format(i=i))
for i, ax in enumerate(bax.first_col):
    ax.yaxis.set_major_locator(ticker.AutoLocator())
    ax.set_ylabel('yscale {i}'.format(i=i))

##############################################################################
# .. note:: It is not necessary to loop through all the axes since they all
#      share the same x and y limits in a given column or row.


##############################################################################
# Manually set the ticks
# ----------------------
#
# Since brokenaxes return normal matplotlib axes, you could also set them
# manually.

fig2 = plt.figure()
bax = make_plot()

bax.first_col[0].set_yticks([80, 85, 90, 95, 100])
bax.first_col[1].set_yticks([-100, -50, 0])

bax.last_row[0].set_xticks([0, 1, 2, 3, 4, 5])
bax.last_row[1].set_xticks([10, 20, 30])
