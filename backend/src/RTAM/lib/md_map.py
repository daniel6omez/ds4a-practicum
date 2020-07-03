import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd

#Recall app
from app import app




#############################
# Load map data
#############################
df = pd.read_csv("Data/accidents_cleanV2.csv", parse_dates=['fecha_incidente'])

with open('Data/Barrios.geojson', encoding='utf8') as geo:
    geojson = json.loads(geo.read())
 
for i, f in enumerate(geojson["features"]):
    f["id"] = f["properties"]["CODIGO"]
    geojson["features"][i] = f

#Map


def update_map(start_date= None, end_date= None):
    dff=df
    if start_date != None and end_date != None:
        dff=df[(df.fecha_incidente >= start_date) & (df.fecha_incidente <= end_date)]
        
    accidents_cn = dff.groupby(["cbml", "barrio"])["radicado"].count().reset_index(name="accidents_count")
    figure6 = px.choropleth_mapbox(accidents_cn,                         #Data
        locations='cbml',                         #Column containing the identifiers used in the GeoJSON file 
        color='accidents_count',                            #Column giving the color intensity of the region
        geojson=geojson,                      #The GeoJSON file
        #featureidkey = "properties.CODIGO", 
        hover_name="barrio",
        hover_data={'cbml':False, 'accidents_count':True },#'sepal_length':':.2f',}
        zoom=10.5,                                   #Zoom
        mapbox_style="carto-positron",            #Mapbox style, for different maps you need a Mapbox account and a token
        center={"lat": 6.2653382, "lon": -75.6035539}, #Center 0
        color_continuous_scale= ['white','yellow','orange','red','darkred'], # "reds"  "Viridis",         #Color Scheme        
        #colorbar_title = "Conteo accidentes",
        opacity=0.5,                              #Opacity of the map
      )
    
    figure6.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, width=1000)
    return figure6

    
    


##############################
#Map Layout
##############################
map=html.Div([
 #Place the main graph component here:
  dcc.Graph(figure=update_map(), id='md_map')
], className="ds4a-body")
    