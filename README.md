# brokenaxes

![brokenaxes logo. Reference: http://www.brianhensley.net/2012/02/python-controlling-spi-bus-on.html](broken_python_snake.png)

brokenaxes makes matplotlib plots with breaks in the axes for showing data across a discontinuous range.

[![PyPI](https://img.shields.io/pypi/v/brokenaxes.svg?style=plastic)](https://pypi.python.org/pypi/brokenaxes)

## Installation
```
pip install brokenaxes
```

## Usage
```python
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import numpy as np

fig = plt.figure(figsize=(5,2))
bax = brokenaxes(xlims=((0, .1), (.4, .7)), ylims=((-1, .7), (.79, 1)), hspace=.05)
x = np.linspace(0, 1, 100)
bax.plot(x, np.sin(10 * x), label='sin')
bax.plot(x, np.cos(10 * x), label='cos')
bax.legend(loc=3)
bax.set_xlabel('time')
bax.set_ylabel('value')
```
![example1](example1.png)

### Features:
* Break x and y axes.
* Supports multiple breaks on a single axis.
* Automatically scales axes according to relative ranges.
* Plot multiple lines.
* Legend with positioning relative to entire broken axes object
* x and y label centered to entire plot
* Make brokenaxes object a subplot itself with `matplotlib.GridSpec.subplot_spec`.
