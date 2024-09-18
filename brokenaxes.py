from datetime import timedelta
from typing import Optional, Tuple, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib import rcParams
from matplotlib import ticker
from matplotlib.figure import Figure

__author__ = "Ben Dichter"


class BrokenAxes:
    def __init__(
        self,
        xlims: Optional[Tuple[Tuple[float, float], ...]] = None,
        ylims: Optional[Tuple[Tuple[float, float], ...]] = None,
        d: float = 0.015,
        tilt: float = 45,
        subplot_spec: Optional[gridspec.GridSpec] = None,
        fig: Optional[Figure] = None,
        despine: bool = True,
        xscale: Optional[str] = None,
        yscale: Optional[str] = None,
        diag_color: str = "k",
        height_ratios: Optional[List[int]] = None,
        width_ratios: Optional[List[int]] = None,
        *args,
        **kwargs
    ):
        """
        Initializes a grid of axes that simulate a single broken axis.

        Parameters
        ----------
        xlims : tuple of tuples, optional
            X-axis limits for each subplot. If `None`, the x-axis is not broken.
        ylims : tuple of tuples, optional
            Y-axis limits for each subplot. If `None`, the y-axis is not broken.
        d : float, default=0.015
            Length of diagonal split mark used to indicate broken axes.
        tilt : float, default=45
            Angle of diagonal split mark.
        subplot_spec : Gridspec.subplot_spec, optional
            Defines a subplot. If `None`, a new subplot specification is created.
        fig : Figure, optional
            The figure object. If `None`, uses the current figure.
        despine : bool, optional
            If `True`, removes the right and top spines.
        xscale : {'linear', 'log'}, optional
            Scaling for the x-axis; 'log' or 'linear'.
        yscale : {'linear', 'log'}, optional
            Scaling for the y-axis; 'log' or 'linear'.
        diag_color : str, optional
            Color of the diagonal lines indicating breaks, default is 'k'.
        height_ratios : list of int, optional
            Height ratios of the subplots. If `None`, the height ratios are determined
            using the `ylims` parameter.
        width_ratios : list of int, optional
            Width ratios of the subplots. If `None`, the width ratios are determined
            using the `xlims` parameter.

        Notes
        -----
        This class facilitates creating plots with discontinuities in either the x or y axis,
        by arranging multiple subplots as a single cohesive plot with clear visual indicators
        for the discontinuities.
        """

        self._spines = None
        self.diag_color: str = diag_color
        self.despine: bool = despine
        self.d: float = d
        self.tilt: float = tilt
        self.fig: Figure = fig if fig is not None else plt.gcf()
        self.diag_handles: List = []

        width_ratios = width_ratios if width_ratios is not None else self._calculate_ratios(xlims, xscale)
        height_ratios = height_ratios if height_ratios is not None else self._calculate_ratios(ylims, yscale)[::-1]

        ncols, nrows = len(width_ratios), len(height_ratios)

        kwargs.update(
            ncols=ncols,
            nrows=nrows,
            height_ratios=height_ratios,
            width_ratios=width_ratios,
        )
        if subplot_spec:
            gs = gridspec.GridSpecFromSubplotSpec(
                subplot_spec=subplot_spec, *args, **kwargs
            )
            self.big_ax = plt.Subplot(self.fig, subplot_spec)
        else:
            gs = gridspec.GridSpec(*args, **kwargs)
            self.big_ax = plt.Subplot(self.fig, gridspec.GridSpec(1, 1)[0])

        [sp.set_visible(False) for sp in self.big_ax.spines.values()]
        self.big_ax.set_xticks([])
        self.big_ax.set_yticks([])
        self.big_ax.patch.set_facecolor("none")

        self.axs = []
        for igs in gs:
            ax = plt.Subplot(self.fig, igs)
            self.fig.add_subplot(ax)
            self.axs.append(ax)
        self.fig.add_subplot(self.big_ax)

        # get last axs row and first col
        self.last_row = []
        self.first_col = []
        for ax in self.axs:
            if ax.get_subplotspec().is_last_row():
                self.last_row.append(ax)
            if ax.get_subplotspec().is_first_col():
                self.first_col.append(ax)

        # Set common x/y lim for ax in the same col/row
        # and share x and y between them
        for i, ax in enumerate(self.axs):
            if ylims is not None:
                ax.set_ylim(ylims[::-1][i // ncols])
                ax.sharey(self.first_col[i // ncols])
            if xlims is not None:
                ax.set_xlim(xlims[i % ncols])
                ax.sharex(self.last_row[i % ncols])
        self.standardize_ticks()
        if d:
            self.draw_diags()
        self.set_spines()

    @staticmethod
    def _calculate_ratios(lims, scale):
        """
        Calculate width or height ratios based on axis limits and scale.

        Parameters
        ----------
        lims : tuple of tuples
            Axis limits for each subplot.
        scale : str
            Scaling for the axis ('linear' or 'log').
        """
        if lims is None:
            return [1]

        if scale == "log":
            ratios = [np.log(i[1]) - np.log(i[0]) for i in lims]
        else:
            ratios = [i[1] - i[0] for i in lims]

        # handle datetime xlims
        if isinstance(ratios[0], timedelta):
            ratios = [tt.total_seconds() for tt in ratios]

        return ratios

    @staticmethod
    def draw_diag(ax, xpos, ypos, xlen, ylen, **kwargs):
        return ax.plot((xpos - xlen, xpos + xlen), (ypos - ylen, ypos + ylen), **kwargs)

    def draw_diags(self, d=None, tilt=None):
        """

        Parameters
        ----------
        d: float
            Length of diagonal split mark used to indicate broken axes
        tilt: float
            Angle of diagonal split mark
        """
        if d is not None:
            self.d = d
        if tilt is not None:
            self.tilt = tilt
        size = self.fig.get_size_inches()

        d_kwargs = dict(
            transform=self.fig.transFigure,
            color=self.diag_color,
            clip_on=False,
            lw=rcParams["axes.linewidth"],
            ylen=self.d * np.sin(self.tilt * np.pi / 180) * size[0] / size[1],
            xlen=self.d * np.cos(self.tilt * np.pi / 180)
        )

        ds = []
        for ax in self.axs:
            bounds = ax.get_position().bounds

            if ax.get_subplotspec().is_last_row():
                ypos = bounds[1]
                if not ax.get_subplotspec().is_last_col():
                    xpos = bounds[0] + bounds[2]
                    ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)
                if not ax.get_subplotspec().is_first_col():
                    xpos = bounds[0]
                    ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)

            if ax.get_subplotspec().is_first_col():
                xpos = bounds[0]
                if not ax.get_subplotspec().is_first_row():
                    ypos = bounds[1] + bounds[3]
                    ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)
                if not ax.get_subplotspec().is_last_row():
                    ypos = bounds[1]
                    ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)

            if not self.despine:
                if ax.get_subplotspec().is_first_row():
                    ypos = bounds[1] + bounds[3]
                    if not ax.get_subplotspec().is_last_col():
                        xpos = bounds[0] + bounds[2]
                        ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)
                    if not ax.get_subplotspec().is_first_col():
                        xpos = bounds[0]
                        ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)

                if ax.get_subplotspec().is_last_col():
                    xpos = bounds[0] + bounds[2]
                    if not ax.get_subplotspec().is_first_row():
                        ypos = bounds[1] + bounds[3]
                        ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)
                    if not ax.get_subplotspec().is_last_row():
                        ypos = bounds[1]
                        ds += self.draw_diag(ax, xpos, ypos, **d_kwargs)
        self.diag_handles = ds

    def set_spines(self):
        """Removes the spines of internal axes that are not boarder spines."""

        # Helper function to hide axis elements
        def hide_axis_elements(axis):
            for element in (axis.get_majorticklines() + axis.get_minorticklines() +
                            axis.get_majorticklabels() + axis.get_minorticklabels()):
                element.set_visible(False)

        for ax in self.axs:
            ax.xaxis.tick_bottom()
            ax.yaxis.tick_left()
            subplotspec = ax.get_subplotspec()
            if not subplotspec.is_last_row():
                ax.spines["bottom"].set_visible(False)
                hide_axis_elements(ax.xaxis)
            if self.despine or not subplotspec.is_first_row():
                ax.spines["top"].set_visible(False)
            if not subplotspec.is_first_col():
                ax.spines["left"].set_visible(False)
                hide_axis_elements(ax.yaxis)
            if self.despine or not subplotspec.is_last_col():
                ax.spines["right"].set_visible(False)

    def standardize_ticks(self, xbase=None, ybase=None):
        """Make all the internal axes share tick bases

        Parameters
        ----------
        xbase, ybase: (optional) None or float
            If `xbase` or `ybase` is a float, manually set all tick locators to
            this base. Otherwise, use the largest base across internal subplots
            for that axis.
        """
        if xbase is None:
            if self.axs[0].xaxis.get_scale() == "log":
                xbase = max(
                    ax.xaxis.get_ticklocs()[1] / ax.xaxis.get_ticklocs()[0]
                    for ax in self.axs
                    if ax.get_subplotspec().is_last_row()
                )
            else:
                xbase = max(
                    ax.xaxis.get_ticklocs()[1] - ax.xaxis.get_ticklocs()[0]
                    for ax in self.axs
                    if ax.get_subplotspec().is_last_row()
                )
        if ybase is None:
            if self.axs[0].yaxis.get_scale() == "log":
                ybase = max(
                    ax.yaxis.get_ticklocs()[1] / ax.yaxis.get_ticklocs()[0]
                    for ax in self.axs
                    if ax.get_subplotspec().is_first_col()
                )
            else:
                ybase = max(
                    ax.yaxis.get_ticklocs()[1] - ax.yaxis.get_ticklocs()[0]
                    for ax in self.axs
                    if ax.get_subplotspec().is_first_col()
                )

        for ax in self.axs:
            if ax.get_subplotspec().is_first_col():
                if ax.yaxis.get_scale() == "log":
                    ax.yaxis.set_major_locator(ticker.LogLocator(ybase))
                else:
                    ax.yaxis.set_major_locator(ticker.MultipleLocator(ybase))
            if ax.get_subplotspec().is_last_row():
                if ax.xaxis.get_scale() == "log":
                    ax.xaxis.set_major_locator(ticker.LogLocator(xbase))
                else:
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(xbase))

    def fix_exponent(self):
        for ax in self.axs:
            subplotspec = ax.get_subplotspec()
            if not (subplotspec.is_first_col() and subplotspec.is_first_row()):
                ax.get_yaxis().get_offset_text().set_visible(False)
            if not (subplotspec.is_last_col() and subplotspec.is_last_row()):
                ax.get_xaxis().get_offset_text().set_visible(False)

    def __getattr__(self, method):
        """Catch all methods that are not defined and pass to internal axes
        (e.g. plot, errorbar, etc.).
        """
        if method in [
            "get_yaxis",
            "get_xaxis",
            "get_shared_x_axes",
            "get_shared_y_axes",
            "get_second_yaxis",
            "get_second_xaxis",
            "get_legend",
            "get_title",
            "get_xlabel",
            "get_ylabel",
        ]:
            return getattr(self.big_ax, method)

        return lambda *args, **kwargs: self.subax_call(method, args, kwargs)

    def subax_call(self, method, args, kwargs):
        """Apply method call to all internal axes. Called by CallCurator."""
        result = []
        for ax in self.axs:
            if ax.xaxis.get_scale() == "log":
                ax.xaxis.set_major_locator(ticker.LogLocator())
            else:
                ax.xaxis.set_major_locator(ticker.AutoLocator())
            if ax.yaxis.get_scale() == "log":
                ax.yaxis.set_major_locator(ticker.LogLocator())
            else:
                ax.yaxis.set_major_locator(ticker.AutoLocator())
            result.append(getattr(ax, method)(*args, **kwargs))

        self.standardize_ticks()
        self.set_spines()
        self.fix_exponent()

        return result

    def set_xlabel(self, label, labelpad=15, **kwargs):
        return self.big_ax.set_xlabel(label, labelpad=labelpad, **kwargs)

    def set_ylabel(self, label, labelpad=30, **kwargs):
        return self.big_ax.set_ylabel(label, labelpad=labelpad, **kwargs)

    def set_title(self, *args, **kwargs):
        return self.big_ax.set_title(*args, **kwargs)

    def legend(self, handles=None, labels=None, *args, **kwargs):
        if handles is None or labels is None:
            h, l = self.axs[0].get_legend_handles_labels()
            if handles is None:
                handles = h
            if labels is None:
                labels = l
        return self.big_ax.legend(handles=handles, labels=labels, *args, **kwargs)

    def secondary_yaxis(
        self, location="right", functions=None, label=None, labelpad=30
    ):
        assert location in ["right", "left"], "location must be 'right' or 'left'"
        if location == "right":
            [
                ax.secondary_yaxis("right", functions=functions)
                for ax in self.axs
                if ax.get_subplotspec().is_last_col()
            ]
        else:
            [
                ax.secondary_yaxis("left", functions=functions)
                for ax in self.axs
                if ax.get_subplotspec().is_first_col()
            ]
        secax = self.big_ax.secondary_yaxis(location, functions=functions)

        secax.spines[location].set_visible(False)
        secax.set_yticks([])
        secax.patch.set_facecolor("none")

        if label is not None:
            secax.set_ylabel(label, labelpad=labelpad)

        return secax

    def secondary_xaxis(self, location="top", functions=None, label=None, labelpad=30):
        assert location in ["top", "bottom"], "location must be 'top' or 'bottom'"
        if location == "top":
            [
                ax.secondary_xaxis("top", functions=functions)
                for ax in self.axs
                if ax.get_subplotspec().is_first_row()
            ]
        else:
            [
                ax.secondary_xaxis("bottom", functions=functions)
                for ax in self.axs
                if ax.get_subplotspec().is_last_row()
            ]
        secax = self.big_ax.secondary_xaxis(location, functions=functions)

        secax.spines[location].set_visible(False)
        secax.set_xticks([])
        secax.patch.set_facecolor("none")

        if label is not None:
            secax.set_xlabel(label, labelpad=labelpad)

        return secax

    def text(self, x, y, s, *args, **kwargs):
        # find axes object that should contain text
        for ax in self.axs:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            if xlim[0] < x < xlim[1] and ylim[0] < y < ylim[1]:
                return ax.text(x, y, s, *args, **kwargs)

        raise ValueError("(x,y) coordinate of text not within any axes")

    @property
    def spines(self):
        if self._spines is None:
            self._spines = dict(
                top=[ax.spines["top"] for ax in self.axs if ax.get_subplotspec().is_first_row()],
                right=[ax.spines["right"] for ax in self.axs if ax.get_subplotspec().is_last_col()],
                bottom=[ax.spines["bottom"] for ax in self.axs if ax.get_subplotspec().is_last_row()],
                left=[ax.spines["left"] for ax in self.axs if ax.get_subplotspec().is_first_col()],
            )
        return self._spines


def brokenaxes(*args, **kwargs):
    """Convenience method for `BrokenAxes` class.

    Parameters
    ----------
    args, kwargs: passed to `BrokenAxes()`

    Returns
    -------
    out: `BrokenAxes`
    """
    return BrokenAxes(*args, **kwargs)
