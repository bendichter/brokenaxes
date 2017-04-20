import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

import numpy as np

class BrokenAxes:
    def __init__(self, xlims=None, ylims=None, d=.015, tilt=45,
                 subplot_spec=None, fig=None, despine=True, *args, **kwargs):

        self.despine = despine
        if fig is None:
            self.fig = plt.gcf()
        else:
            self.fig = fig

        if xlims:
            width_ratios = [i[1] - i[0] for i in xlims]
        else:
            width_ratios = [1]

        if ylims:
            height_ratios = [i[1] - i[0] for i in ylims[::-1]]
        else:
            height_ratios = [1]

        ncols, nrows = len(width_ratios), len(height_ratios)

        kwargs.update(ncols=ncols, nrows=nrows, height_ratios=height_ratios,
                      width_ratios=width_ratios)
        if subplot_spec:
            gs = gridspec.GridSpecFromSubplotSpec(subplot_spec=subplot_spec,
                                                  *args, **kwargs)
            self.big_ax = plt.Subplot(self.fig, subplot_spec)
        else:
            gs = gridspec.GridSpec(*args, **kwargs)
            self.big_ax = plt.Subplot(self.fig, gridspec.GridSpec(1,1)[0])

        [sp.set_visible(False) for sp in self.big_ax.spines.values()]
        self.big_ax.set_xticks([])
        self.big_ax.set_yticks([])
        self.big_ax.patch.set_facecolor('none')

        self.axs = []
        for igs in gs:
            ax = plt.Subplot(self.fig, igs)
            self.fig.add_subplot(ax)
            self.axs.append(ax)
        self.fig.add_subplot(self.big_ax)

        bounds = self.big_ax.get_position().bounds

        for i, ax in enumerate(self.axs):
            if ylims is not None:
                ax.set_ylim(ylims[::-1][i//ncols])
            if xlims is not None:
                ax.set_xlim(xlims[i % ncols])
        self.standardize_ticks()
        if d:
            self.draw_diags(d, tilt)
        if despine:
            self.set_spines()

    def draw_diags(self, d, tilt):
        size = self.fig.get_size_inches()
        ylen = d * np.sin(tilt * np.pi / 180) * size[0] / size[1]
        xlen = d * np.cos(tilt * np.pi / 180)
        d_kwargs = dict(transform=self.fig.transFigure, color='k', clip_on=False)
        for ax in self.axs:
            bounds = ax.get_position().bounds
            if ax.is_last_row():
                ypos = bounds[1]
                if not ax.is_last_col():
                    xpos = bounds[0] + bounds[2]
                    ax.plot((xpos - xlen, xpos + xlen), (ypos - ylen, ypos + ylen),
                             **d_kwargs)
                if not ax.is_first_col():
                    xpos = bounds[0]
                    ax.plot((xpos - xlen, xpos + xlen), (ypos - ylen, ypos + ylen),
                             **d_kwargs)

            if ax.is_first_col():
                xpos = bounds[0]
                if not ax.is_first_row():
                    ypos = bounds[1] + bounds[3]
                    ax.plot((xpos - xlen, xpos + xlen), (ypos - ylen, ypos + ylen),
                             **d_kwargs)
                if not ax.is_last_row():
                    ypos = bounds[1]
                    ax.plot((xpos - xlen, xpos + xlen), (ypos - ylen, ypos + ylen),
                             **d_kwargs)

    def set_spines(self):
        for ax in self.axs:
            ax.xaxis.tick_bottom()
            ax.yaxis.tick_left()
            if not ax.is_last_row():
                ax.spines['bottom'].set_visible(False)
                ax.set_xticks([])
            if self.despine or not ax.is_first_row():
                ax.spines['top'].set_visible(False)
            if not ax.is_first_col():
                ax.spines['left'].set_visible(False)
                ax.set_yticks([])
            if self.despine or not ax.is_last_col():
                ax.spines['right'].set_visible(False)

    def standardize_ticks(self, xbase=None, ybase=None):
        if xbase is None:
            xbase = max(ax.xaxis.get_ticklocs()[1] - ax.xaxis.get_ticklocs()[0]
                        for ax in self.axs if ax.is_last_row())
        if ybase is None:
            ybase = max(ax.yaxis.get_ticklocs()[1] - ax.yaxis.get_ticklocs()[0]
                        for ax in self.axs if ax.is_first_col())

        for ax in self.axs:
            if ax.is_first_col():
                ax.yaxis.set_major_locator(ticker.MultipleLocator(ybase))
            if ax.is_last_row():
                ax.xaxis.set_major_locator(ticker.MultipleLocator(xbase))

    def plot(self, *args, **kwargs):
        for ax in self.axs:
            ax.xaxis.set_major_locator(ticker.AutoLocator())
            ax.yaxis.set_major_locator(ticker.AutoLocator())
            ax.plot(*args, **kwargs)

        self.standardize_ticks()
        self.set_spines()

    def set_xlabel(self, label, labelpad=20, **kwargs):
        self.big_ax.set_xlabel(label, labelpad=labelpad, **kwargs)

    def set_ylabel(self, label, labelpad=30, **kwargs):
        self.big_ax.xaxis.labelpad = labelpad
        self.big_ax.set_ylabel(label, labelpad=labelpad, **kwargs)

    def set_title(self, *args, **kwargs):
        self.big_ax.set_title(*args, **kwargs)

    def legend(self, *args, **kwargs):
        h, l = self.axs[0].get_legend_handles_labels()
        self.big_ax.legend(h, l, *args, **kwargs)

    def axis(self, *args, **kwargs):
        [ax.axis(*args, **kwargs) for ax in self.axs]


def brokenaxes(*args, **kwargs):
    return BrokenAxes(*args, **kwargs)
