import random

from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure, show
import numpy as np


def create_plot():
    source = ColumnDataSource(dict(
        time=[0, 1, 2], velocitycommand=[0, 1, 2]
    ))
    p = figure(height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_type=None, y_axis_location="right")
    p.x_range.follow = "end"
    p.x_range.follow_interval = 100
    p.x_range.range_padding = 0

    p.line(x='time', y='velocitycommand', alpha=0.2, line_width=3, color='navy', source=source)

    show(p)

    return source

def update_plot(curtime, source):
    update = {
        'time' : [curtime],
        'velocitycommand' : 10*random.random()
    }

    source.stream(update)

