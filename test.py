import datetime

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.gridspec import GridSpec
import matplotlib as mpl

from brokenaxes import brokenaxes


np.random.seed(42)


@pytest.mark.mpl_image_compare
def test_standard():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    x = np.linspace(0, 1, 100)
    bax.plot(x, np.sin(10 * x), label="sin")
    bax.plot(x, np.cos(10 * x), label="cos")
    bax.legend(loc=3)
    bax.set_xlabel("time")
    bax.set_ylabel("value")
    return fig


@pytest.mark.mpl_image_compare
def test_subplots():
    sps1, sps2 = GridSpec(2, 1)

    bax = brokenaxes(xlims=((0.1, 0.3), (0.7, 0.8)), subplot_spec=sps1)
    x = np.linspace(0, 1, 100)
    bax.plot(x, np.sin(x * 30), ls=":", color="m")

    x = np.random.poisson(3, 1000)
    bax = brokenaxes(xlims=((0, 2.5), (3, 6)), subplot_spec=sps2)
    bax.hist(x, histtype="bar")

    return bax.fig


@pytest.mark.mpl_image_compare
def test_log():
    fig = plt.figure(figsize=(5, 5))
    bax = brokenaxes(
        xlims=((1, 500), (600, 10000)),
        ylims=((1, 500), (600, 10000)),
        hspace=0.15,
        xscale="log",
        yscale="log",
    )

    x = np.logspace(0.0, 4, 100)
    bax.loglog(x, x, label="$y=x=10^{0}$ to $10^{4}$")

    bax.legend(loc="best")
    bax.grid(axis="both", which="major", ls="-")
    bax.grid(axis="both", which="minor", ls="--", alpha=0.4)
    bax.set_xlabel("x")
    bax.set_ylabel("y")

    return fig


@pytest.mark.mpl_image_compare
def test_datetime():
    fig = plt.figure(figsize=(5, 5))
    xx = [datetime.datetime(2020, 1, x) for x in range(1, 20)]

    yy = np.arange(1, 20)

    bax = brokenaxes(
        xlims=(
            (
                datetime.datetime(2020, 1, 1),
                datetime.datetime(2020, 1, 3),
            ),
            (
                datetime.datetime(2020, 1, 6),
                datetime.datetime(2020, 1, 20),
            ),
        ),
    )

    bax.plot(xx, yy)
    fig.autofmt_xdate()

    [x.remove() for x in bax.diag_handles]
    bax.draw_diags()

    return fig


@pytest.mark.mpl_image_compare
def test_datetime_y():
    fig = plt.figure(figsize=(5, 5))
    yy = [datetime.datetime(2020, 1, x) for x in range(1, 20)]

    xx = np.arange(1, 20)

    bax = brokenaxes(
        ylims=(
            (
                datetime.datetime(2020, 1, 1),
                datetime.datetime(2020, 1, 3),
            ),
            (
                datetime.datetime(2020, 1, 6),
                datetime.datetime(2020, 1, 20),
            ),
        )
    )

    bax.plot(xx, yy)

    bax.draw_diags()

    return fig


@pytest.mark.mpl_image_compare
def test_legend():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    x = np.linspace(0, 1, 100)
    h1 = bax.plot(x, np.sin(10 * x), label="sin")
    h2 = bax.plot(x, np.cos(10 * x), label="cos")
    bax.legend(handles=[h1[0][0], h2[0][0]], labels=["1", "2"])

    return fig


@pytest.mark.mpl_image_compare
def test_text():
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    bax.text(0.5, 0.5, "hello")

    return bax.fig


@pytest.mark.mpl_image_compare
def test_lims_arrays():
    lims = np.arange(6).reshape((-1, 2))
    brokenaxes(xlims=lims, ylims=lims)

    return plt.gcf()


@pytest.mark.mpl_image_compare
def test_pass_fig():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05, fig=fig
    )
    assert bax.fig is fig

    return fig


@pytest.mark.mpl_image_compare
def test_despine():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05, despine=False,
    )
    assert bax.despine is False

    return fig


@pytest.mark.mpl_image_compare
def test_set_title():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    bax.set_title("title")

    return fig


@pytest.mark.mpl_image_compare
def test_secondary_axes():

    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    bax.secondary_xaxis("top", label="top")
    print(type(isinstance(bax.secondary_xaxis(), mpl.axis.XAxis)))
    bax.secondary_xaxis("bottom")
    bax.secondary_yaxis("left", label="left")
    bax.secondary_yaxis("right")

    return fig


@pytest.mark.mpl_image_compare
def test_text():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)))
    bax.text(0.5, 0.5, "hello")

    return fig


@pytest.mark.mpl_image_compare
def test_draw_diags():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    bax.draw_diags(tilt=90, d=.05)

    return fig


@pytest.mark.mpl_image_compare
def test_set_spine_prop():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )

    [x.set_linewidth(2) for x in bax.spines["bottom"]]

    return fig


@pytest.mark.mpl_image_compare
def test_fig_tight_layout():
    fig = plt.figure()

    subplot_specs = GridSpec(2, 2)

    baxs = []

    xlims = ((.1, .3),(.7, .8))
    x = np.linspace(0, 1, 100)

    for color, sps in zip(['red', 'green', 'blue', 'magenta'], subplot_specs):

        bax = brokenaxes(xlims=xlims, subplot_spec=sps)
        bax.plot(x, np.sin(x*30), color=color)
        baxs.append(bax)

    plt.tight_layout()
    for bax in baxs:
        for handle in bax.diag_handles:
            handle.remove()
        bax.draw_diags()

    return fig


def test_get_axis_special():
    fig = plt.figure(figsize=(5, 2))
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    assert isinstance(bax.get_yaxis(), mpl.axis.YAxis)
    assert isinstance(bax.get_shared_x_axes(), mpl.cbook.GrouperView)
    assert isinstance(bax.get_xaxis(), mpl.axis.XAxis)
    assert isinstance(bax.get_shared_y_axes(), mpl.cbook.GrouperView)


def test_text_error():
    bax = brokenaxes(
        xlims=((0, 0.1), (0.4, 0.7)), ylims=((-1, 0.7), (0.79, 1)), hspace=0.05
    )
    with pytest.raises(ValueError):
        bax.text(-11, -11, "hello")


def test_single_tick_handling():
    """Test that brokenaxes handles axes with only a single tick without raising IndexError.
    
    This addresses the issue where standardize_ticks() would fail with IndexError
    when an axis has only one tick location, due to trying to access get_ticklocs()[1]
    when the array has only one element.
    """
    # Test case 1: Force single tick on both axes
    fig = plt.figure(figsize=(5, 3))
    bax = brokenaxes(xlims=((0, 1),), ylims=((0, 1),))

    # Manually set single ticks to trigger the issue
    for ax in bax.axs:
        ax.set_xticks([0.5])
        ax.set_yticks([0.5])

    # This should not raise IndexError
    bax.standardize_ticks()
    plt.close(fig)

    # Test case 2: Very small range that might result in single tick
    fig = plt.figure(figsize=(5, 3))
    bax = brokenaxes(xlims=((0, 1e-10),), ylims=((0, 1e-10),))
    bax.plot([0], [0], 'o')
    plt.close(fig)

    # Test case 3: Log scale with single tick
    fig = plt.figure(figsize=(5, 3))
    bax = brokenaxes(xlims=((1, 10),), ylims=((1, 10),), xscale='log', yscale='log')

    for ax in bax.axs:
        ax.set_xticks([5])
        ax.set_yticks([5])

    # This should not raise IndexError for log scale either
    bax.standardize_ticks()
    plt.close(fig)
