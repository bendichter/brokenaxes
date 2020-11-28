"""
Second Y Axis
=============

You can use the following technique to give your brokenaxes plot a second axis on the right.
Analogous code works for creating a secondary x axis.

"""

from brokenaxes import brokenaxes

functions = (lambda x: x*0.453592, lambda x: x/0.453592)


bax = brokenaxes(
    xlims=((1, 3), (9, 10)),
    ylims=((1, 3), (9, 10)),
    despine=False
    )

bax.plot(range(11))
bax.set_ylabel('pounds')
secax = bax.secondary_yaxis(functions=functions, label='kg')


