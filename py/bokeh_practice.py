import math
import numpy as np
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.sampledata.stocks import MSFT


def run_bokeh():

    df = pd.DataFrame(MSFT)[:100]
    df["date"] = pd.to_datetime(df["date"])

    inc = df.close >= df.open
    dec = df.close < df.open
    w = 12*60*60*1000

    TOOLS = "pan, wheel_zoom, box_zoom, reset"

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, height=400, title="MSFT Candlestick")
    p.xaxis.major_label_orientation = math.pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.date, df.high, df.date, df.low, color="black")
    p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    script1, div1 = components(p)
    return script1, div1
