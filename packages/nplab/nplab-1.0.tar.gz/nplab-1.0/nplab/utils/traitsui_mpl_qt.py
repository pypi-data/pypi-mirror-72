#!/usr/bin/python
# -*- coding: utf-8 -*-
# Pierre Haessig — March 2014
"""
Qt adaptation of Gael Varoquaux's tutorial to integrate Matplotlib
http://docs.enthought.com/traitsui/tutorials/traits_ui_scientific_app.html#extending-traitsui-adding-a-matplotlib-figure-to-our-application

based on Qt-based code shared by Didrik Pinte, May 2012
http://markmail.org/message/z3hnoqruk56g2bje

adapted and tested to work with PySide from Anaconda in March 2014
"""

from nplab.utils.gui import *

import matplotlib
# We want matplotlib to use a QT backend
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from traits.api import Any, Instance
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory


class FigureCanvasWithDeferredDraw(FigureCanvas):
    # This class allows us to use Qt's event loop to draw the canvas from
    # the GUI thread, even if the call comes from outside the GUI thread.
    # this is necessary if you want to plot from a background thread.
    ask_for_redraw = QtCore.Signal()
    
    def __init__(self, figure):
        FigureCanvas.__init__(self, figure)
        # We connect the ask_for_redraw signal to the FigureCanvas's draw() method.
        # using a QueuedConnection ensures that draw() is correctly called in the
        # application's main GUI thread.
        self.ask_for_redraw.connect(self.draw, type=QtCore.Qt.QueuedConnection)

    def draw_in_main_loop(self):
        """Draw the canvas, but do so in the Qt main loop to avoid threading nasties."""
        self.ask_for_redraw.emit()


class _MPLFigureEditor(Editor):

    scrollable = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # matplotlib commands to create a canvas
        mpl_canvas = FigureCanvasWithDeferredDraw(self.value)
        return mpl_canvas


class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor


if __name__ == "__main__":
    # Create a window to demo the editor
    from traits.api import HasTraits, Int, Float, on_trait_change
    from traitsui.api import View, Item
    from numpy import sin, cos, linspace, pi

    class Test(HasTraits):

        figure = Instance(Figure, ())
        n = Int(11)
        a = Float(0.5)

        view = View(Item('figure', editor=MPLFigureEditor(),
                         show_label=False),
                    Item('n'),
                    Item('a'),
                    width=400,
                    height=300,
                    resizable=True)

        def __init__(self):
            super(Test, self).__init__()
            axes = self.figure.add_subplot(111)
            self._t = linspace(0, 2 * pi, 200)
            self.plot()

        @on_trait_change('n,a')
        def plot(self):
            t = self._t
            a = self.a
            n = self.n
            axes = self.figure.axes[0]
            if not axes.lines:
                axes.plot(sin(t) * (1 + a * cos(n * t)), cos(t) * (1 + a * cos(n * t)))
            else:
                l = axes.lines[0]
                l.set_xdata(sin(t) * (1 + a * cos(n * t)))
                l.set_ydata(cos(t) * (1 + a * cos(n * t)))
            canvas = self.figure.canvas
            if canvas is not None:
                canvas.draw()

    t = Test()
    t.configure_traits()
