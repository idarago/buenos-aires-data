import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

data = gpd.read_file("./Datasets/covid_data_by_neighborhood.geojson")

import json
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider, Range1d)
# Getting the geographic data we're going to plot
geosource = GeoJSONDataSource(geojson = data.to_json())

from bokeh.io import show, save
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_notebook, reset_output, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html, components

def covidPlotter(field, title, filename):
    # Define color palettes
    palette = brewer['OrRd'][8]
    palette = palette[::-1] # reverse order of colors so higher values have darker colors

    # Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette)#, low = 0, high = 900)
    color_bar = ColorBar(color_mapper = color_mapper, 
                        label_standoff = 12)
    # Create figure object.
    p = figure(#title = titulo, 
            plot_height = 600, plot_width = 600, 
            toolbar_location = None)
    p.title.text = title
    p.title.align = "center"
    p.title.text_font_size = "16px"

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # Make axis invisible
    p.xaxis.visible = False
    p.xgrid.visible = False
    p.yaxis.visible = False
    p.ygrid.visible = False

    # Add patch renderer to figure.
    renderer = p.patches('xs','ys', source = geosource,
                    fill_color = {'field' :field,
                                    'transform' : color_mapper},
                    line_color = 'gray', 
                    line_width = 0.5, 
                    fill_alpha = 1)
    # Create hover tool
    p.add_tools(HoverTool(renderers = [renderer],
                        tooltips = [('Neighborhood','@barrio'),
                                    ('Cases', '@cases'),
                                    ('Deaths', '@deaths'),
                                ('Population', '@population')]))

    # Specify layout
    p.add_layout(color_bar, 'right')
    output_file(filename+".html",title=title,mode='inline')
    show(p)
    script, div = components(p)

    outFile = open(filename+"_script.html",'w')
    outFile.write(script)
    outFile.close()

    outFile2 = open(filename+"_div.html",'w')
    outFile2.write(div)
    outFile2.close()


field = "death_density"
title = "Covid deaths by neighborhood in Buenos Aires per 1000 people"
filename = "covid_deaths_by_neighborhood.html"
covidPlotter(field, title, filename)