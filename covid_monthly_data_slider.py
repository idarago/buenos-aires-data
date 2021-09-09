import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

ordered_months = ["Mar2020", 
                   "Apr2020", 
                   "May2020", 
                   "Jun2020", 
                   "Jul2020",
                   "Aug2020",
                   "Sep2020",
                   "Oct2020",
                   "Nov2020",
                   "Dec2020",
                   "Jan2021",
                   "Feb2021",
                   "Mar2021", 
                   "Apr2021", 
                   "May2021", 
                   "Jun2021", 
                   "Jul2021"]

months_name = ["March 2020", "April 2020", "May 2020", "June 2020", "July 2020", "August 2020", "September 2020", "October 2020", "November 2020", "December 2020", "January 2021", "February 2021", "March 2021", "April 2021",  "May 2021", "June 2021", "July 2021"]

data = gpd.read_file("./Datasets/cases_by_month.geojson")

monthly_data = {month : data[["barrio","geometry","population",month]] for month in ordered_months}
for month in ordered_months:
    monthly_data[month] = monthly_data[month].rename(columns={month:"casos"})


import json
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider, Range1d)
from bokeh.io import show, save
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_notebook, reset_output, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html, components

# Getting the geographic data we're going to plot
datalist = {i : monthly_data[ordered_months[i]].to_json() for i in range(len(ordered_months))}
currmonth = len(ordered_months)-1

source = GeoJSONDataSource(geojson=datalist[currmonth])

# Define color palettes
palette = brewer['YlGn'][8]
palette = palette[::-1] # reverse order of colors so higher values have darker colors
color_mapper = LinearColorMapper(palette = palette, low=0, high=4000)
color_bar = ColorBar(color_mapper = color_mapper, label_standoff = 12)

p = figure(plot_height = 600, plot_width = 600, toolbar_location = None)

# Title
p.title.text = f"COVID-19 new cases in Buenos Aires - {months_name[currmonth]}"
p.title.align = "center"
p.title.text_font_size = "16px"

# Make axis invisible
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False

states = p.patches('xs','ys', source = source,
                fill_color = {'field' : 'casos',
                                'transform' : color_mapper},
                line_color = 'gray', 
                line_width = 0.5, 
                fill_alpha = 1)

p.add_tools(HoverTool(renderers = [states],
                    tooltips = [('Neighborhood','@barrio'),
                            ('Cases', '@casos'),
                            ('Population', '@population')]))

p.add_layout(color_bar, 'right')

slider = Slider(start=0, end=len(ordered_months)-1, value=currmonth, step=1, title="Month", show_value=False, sizing_mode = "stretch_width", tooltips=False)
callback = CustomJS(args=dict(source=source, slider=slider, title=p.title, datalist=datalist, plot=p, color_mapper=color_mapper, months_name=months_name),
                    code="""
    var months_name = months_name;
    var datalist = datalist;
    const A = slider.value;
    source.geojson = datalist[A];
    title.text = "COVID-19 cases in Buenos Aires - " + months_name[A];
    source.change.emit();
""")
#source.trigger("change");
slider.js_on_change('value', callback)


layout = column(
    p,
    row(slider),
)

output_file("covid_monthly_cases.html",title="Covid data by month", mode='inline')
show(layout)
save(layout)    

script, div = components(layout)

outFile = open("covid_monthly_cases_script.html",'w')
outFile.write(script)
outFile.close()

outFile2 = open("covid_monthly_cases_div.html",'w')
outFile2.write(div)
outFile2.close()
