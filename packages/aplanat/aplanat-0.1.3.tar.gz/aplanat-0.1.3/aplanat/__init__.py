"""Simple bokeh plotting API."""

import functools
import os
import warnings

import bokeh.io as bkio
from bokeh.layouts import gridplot
from bokeh.model import Model
from bokeh.models import Range1d
from bokeh.models.annotations import Label
from bokeh.plotting import figure
import fontawesome.icons as fontawesome
from pkg_resources import resource_filename
from si_prefix import si_format

__version__ = '0.1.3'

# we don't run a comprehensive test suite and mostly in notebooks,
# so show warnings all the time.
warnings.simplefilter('always', DeprecationWarning)


def with_fontawesome(f):
    """Decorate a plotting function ensuring font awesome is available.

    The function achieves two things: i) triggers the building of bokeh
    custom model which simply includes font awesome and ii) manipulates
    the current working directory to ensure when the extension build is
    triggered (by a call to bokeh.show) we are running somewhere that is
    writeable, otherwise node complains.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        wd = os.getcwd()
        os.chdir(os.path.expanduser("~"))

        class LoadFontAwesome(Model):
            """Interpreting this will make the FontAwesome fonts available."""

            __implementation__ = resource_filename(
                "aplanat", "fontawesome_icon.ts")
            __dependencies__ = {"font-awesome": "^4.6.3"}

        exc = None
        try:
            val = f(*args, **kwargs)
        except Exception as e:
            exc = e
        os.chdir(wd)

        if exc is not None:
            raise exc
        return val
    return wrapper


@with_fontawesome
def bootstrap_fontawesome():
    """Create a 'plot' just to bootstrap fontawesome."""
    p = figure(
        output_backend='webgl',
        plot_width=200, plot_height=10,
        title=None, toolbar_location=None)
    p.axis.visible = False
    p.grid.visible = False
    p.outline_line_color = None
    p.rect([0.5], [0.5], [1.0], [1.0], fill_color=None)
    p.add_layout(
        Label(
            x=0, y=0.3, text_font="FontAwesome", text_color=None,
            text="{} FontAwesome loaded".format(fontawesome['check'])))
    show(p)


class Grid(list):
    """Create a list of lists of fixed length."""

    def __init__(self, width=4):
        """Initialize the Grid."""
        self.width = width
        self.append(list())

    def add(self, item):
        """Add an item to the grid.

        :param item: item to add

        """
        self[-1].append(item)
        if len(self[-1]) == self.width:
            self.append(list())

    def extend(self, items):
        """Add multiple items.

        :param items: items to add.

        """
        for item in items:
            self.add(item)


def show(plot):
    """Show a plot in a notebook."""
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)


def grid(plots, ncol=4, display=True, **kwargs):
    """Show a grid of plots in a notebook.

    :param plots: a list of bokeh plots.
    :param ncol: number of columns.
    :param kwargs: kwargs for bokeh `gridplot`.

    """
    warnings.warn(
        "Please use `bokeh.layout.gridplot` directly with an optional "
        "call to `.show()`", DeprecationWarning)

    grid = Grid(width=ncol)
    grid.extend(plots)
    plot = gridplot(grid, **kwargs)
    if display:
        show(plot)
    else:
        return plot


class InfoGraphItems(dict):
    """Helper class to cumulatively create items for and infographic."""

    def __init__(self, *args, **kwargs):
        """Initialize the helper, and bootstrap fontawesome."""
        try:
            bootstrap_fontawesome()
        except ImportError:
            pass
        super().__init__(*args, **kwargs)

    def append(self, label, value, icon, unit=''):
        """Add an item.

        :param label: infographic item label.
        :param value: numerical value of headline number (without SI units).
        :param icon: font-awesome icon to use.
        :param unit: additional suffix after SI unit suffix, e.g. "bases".

        """
        self[label] = (label, value, icon, unit)

    def extend(self, items):
        """Add multiple items at once.

        :param items: iterable of 4-tuples, as required by `.add()`.
        """
        for i in items:
            self.append(*i)


@with_fontawesome
def infographic(items, **kwargs):
    """Create and infographic 'plot'.

    :param items: 3-tuples of (label, value, unit, icon); the label should be
        a one or two word description, the value the headline number, and the
        icon the name of a fontawesome icon. If `value` is  numeric, it
        will be normalised by use of an SI suffix for display after which
        `unit` will be appended. If `value` is a string it will be used as is.
    :param kwargs: kwargs for bokeh gridplot.

    ..note:: If `bootstrap_fontawesome` has not already been called, the
        function will load the required fonts, however they will not display
        the first time an Jupyter labs cell is run. If using the
        `InfoGraphItems` helper class, this wrinkle will be taken care of
        provided the helper is initiated in a previous cell.

    """
    plots = list()
    seen = set()
    for label, value, icon, unit in items:
        if label in seen:
            continue
        if not isinstance(value, str):
            value = si_format(value) + unit
        seen.add(label)
        p = figure(
            output_backend='webgl',
            plot_width=175, plot_height=100,
            title=None, toolbar_location=None)
        p.axis.visible = False
        p.grid.visible = False
        p.outline_line_color = None
        p.rect([0.5], [0.5], [1.0], [1.0], fill_color="#2171b5")
        p.x_range = Range1d(start=0.1, end=0.9, bounds=(0.1, 0.9))
        p.y_range = Range1d(start=0.1, end=0.9, bounds=(0.1, 0.9))
        p.add_layout(
            Label(
                x=0.15, y=0.45, text=value, text_color="#DEEBF7",
                text_font_size="24px"))
        p.add_layout(
            Label(
                x=0.15, y=0.2, text=label, text_color="#C6DBEF",
                text_font_size="16px"))
        p.add_layout(
            Label(
                x=0.65, y=0.4, text=fontawesome[icon], text_color="#6BAED6",
                text_font="FontAwesome", text_font_size="48px"))
        plots.append(p)
    defaults = {'toolbar_location': None, "ncols": len(items)}
    defaults.update(kwargs)
    return gridplot(plots, **defaults)
