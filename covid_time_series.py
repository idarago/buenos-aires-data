import numpy as np
import pandas as pd
from bokeh.io import show, save, output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure
from bokeh.embed import components

serie = pd.read_csv("./Datasets/cases_by_date.csv")
dates = np.array(serie['date'], dtype=np.datetime64)
source = ColumnDataSource(data=dict(date=dates, cases=serie['cases'], MA = serie['casesMA']))

p = figure(plot_height=300, plot_width=800, tools="xpan", toolbar_location=None,
           x_axis_type="datetime", x_axis_location="above",
           background_fill_color="#fafafa", x_range=(dates[-200], dates[-1]))

p.line('date', 'cases', source=source, legend_label="Number of cases")
p.line('date', 'MA', source=source, color="orange", legend_label="7-day moving average")
p.legend.click_policy="hide"
p.yaxis.axis_label = 'Cases'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=130, plot_width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'cases', source=source)
select.line('date', 'MA', source=source, color="orange")
select.ygrid.grid_line_color = None
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

output_file("casesbydate.html","Cases by date",mode="inline")
layout = (column(p, select))
show(layout)

script, div = components(layout)

outFile = open("covid_cases_by_date_script.html",'w')
outFile.write(script)
outFile.close()

outFile2 = open("covid_cases_by_date_div.html",'w')
outFile2.write(div)
outFile2.close()
