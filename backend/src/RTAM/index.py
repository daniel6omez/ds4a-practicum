#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#Data 
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#Recall app
from app import app, server

###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from modules import title, sidebar, md_map, heat_maps#, stats

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      md_map.map,
      heat_maps.heatmaps,
      #stats.stats,
      title.title,
      sidebar.sidebar,
    ],
    className="ds4a-app", #You can also add your own css files by locating them into the assets folder
)

 
    
###############################################   
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
#Load and modify the data that will be used in the app.
#################################################################
#df = pd.read_csv('Data/superstore.csv', parse_dates=['Order Date', 'Ship Date'])

#with open('Data/us.json') as geo:
 #   geojson = json.loads(geo.read())

#with open('Data/states.json') as f:
 #   states_dict = json.loads(f.read())

#df['State_abbr'] = df['State'].map(states_dict)
#df['Order_Month'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))



#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@app.callback(
    [Output("MonthDayHeat", "figure"), Output("DayHourHeat", "figure"),Output("LineGraph", "figure")],
    #[Output("MonthDayHeat", "figure"),Output("Scatter","figure"), Output("Treemap",'figure')],
    [
        #Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def update_heat_maps(start_date, end_date):
    MonthDayHeat = heat_maps.update_month_day_heat(start_date, end_date)
    DayHourHeat = heat_maps.update_day_hour_heat(start_date, end_date)
    LineGraph = heat_maps.update_line_graph(start_date, end_date)

    return [MonthDayHeat,DayHourHeat,LineGraph]



#############################################################
# TREEMAP PLOT : Add sidebar interaction here
#############################################################



#############################################################
# MAP : Add interactions here
#############################################################

#MAP date interaction
@app.callback(
    Output("md_map", "figure"),
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def update_map(start_date,end_date):
    return md_map.update_map(start_date,end_date)


#MAP click interaction

@app.callback(
    Output('state_dropdown','value'),
    [
        Input('md_map','clickData')
    ],
    [
        State('state_dropdown','value')
    ]

)
def click_saver(clickData,state):
    if clickData is None:
        raise PreventUpdate
    
    #print(clickData)
    
    state.append(clickData['points'][0]['location'])
    
    return state

if __name__ == "__main__":
    # http_server = WSGIServer(('', 8080), app.server)
    # http_server.serve_forever()
    app.run_server()
    #use the bottom option when debbuging
    # app.run_server(host='localhost',port='8050',debug=True,use_reloader=True)
