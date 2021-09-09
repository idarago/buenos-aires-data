import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shapely

import json
from bokeh.models import (CDSView, ColorBar, ColumnDataSource, MultiLine,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider, Range1d)

from bokeh.io import show, save
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_notebook, reset_output, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html, components

#datos_censales = gpd.read_file("./Datasets/census_data_2001.geojson")
#datos_censales["DENSIDAD"] = 1000*datos_censales["POB_TOT"] / (datos_censales["AREA"])

datos_censales = gpd.read_file("./Datasets/caba_radios_censales.geojson")
datos_censales["DENSIDAD"] = datos_censales["POBLACION"] / (1000*datos_censales["AREA_KM2"])

subte_colores = {"A":"cyan", "B":"red", "C":"blue", "D":"green", "E":"purple", "H":"gold"}

#subte_estaciones = gpd.read_file("./Datasets/subte_estaciones2001.geojson")
#subte_lineas = gpd.read_file("./Datasets/subte_lineas2001.geojson")

subte_estaciones = gpd.read_file("./Datasets/subte_estaciones2010.geojson")
subte_lineas = gpd.read_file("./Datasets/subte_lineas2010.geojson")


estaciones_por_linea =  {linea : subte_estaciones[subte_estaciones["LINEA"]==linea] for linea in ["A","B","C","D","E","H"]}
trayectos_por_linea = {linea : subte_lineas[subte_lineas["LINEASUB"]=="LINEA "+linea] for linea in ["A","B","C","D","E","H"]}

geosource = GeoJSONDataSource(geojson = datos_censales.to_json())

palette = brewer['OrRd'][8]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette = palette, low=0, high=200)
color_bar = ColorBar(color_mapper = color_mapper, label_standoff = 12)

p = figure(plot_height = 600, plot_width = 600, toolbar_location = "right")

p.title.text = "Population density in Buenos Aires (2010)"
p.title.align = "center"
p.title.text_font_size = "16px"


p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False

# Add patch renderer to figure.
renderer = p.patches('xs','ys', source = geosource, fill_color = {'field' :"DENSIDAD", 'transform' : color_mapper},line_color = 'gray', line_width = 0.01, fill_alpha = 1)

for linea in estaciones_por_linea:
    p.circle("x","y",source=GeoJSONDataSource(geojson=estaciones_por_linea[linea].to_json()), color=subte_colores[linea], size=5, alpha=0.5, legend_label="Subte "+linea)
    p.multi_line("xs","ys",source=GeoJSONDataSource(geojson=trayectos_por_linea[linea].to_json()), line_color=subte_colores[linea], line_width=3, legend_label="Subte "+linea)

p.legend.click_policy="hide"

p.add_layout(color_bar, 'right')
output_file("MapaDensidadPoblacion"+".html",title="Population density Buenos Aires 2010",mode='inline')
show(p)

script, div = components(p)

outFile = open("MapaDensidadPoblacion_script.html",'w')
outFile.write(script)
outFile.close()

outFile2 = open("MapaDensidadPoblacion_div.html",'w')
outFile2.write(div)
outFile2.close()