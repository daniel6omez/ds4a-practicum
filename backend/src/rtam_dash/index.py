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
from db.data import df, dff

###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from modules import md_map, heat_maps

x0 = 'xaxis.range[0]'
x1 = 'xaxis.range[1]'

months={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "June":6, "July":7, "Aug":8, "Sept":9, "Oct":10, "Nov":11, "Dec":12}
days={"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
order_days = {'0Monday':0, '1Tuesday':1, '2Wednesday':2, '3Thursday':3, '4Friday':4, '5Saturday':5, '6Sunday':6}
    

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      md_map.map,
      heat_maps.heatmaps
    ],
    className="ds4a-body", #You can also add your own css files by locating them into the assets folder
)


    
###############################################   
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
#Load and modify the data that will be used in the app.
#################################################################

#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@app.callback(
    [Output("md_map", "figure"),Output("month_day_heat", "figure"), Output("day_hour_heat", "figure"),Output("line_graph", "figure")],
    [
        Input('md_map', 'clickData'),
        Input('md_map', 'selectedData'),
        Input('line_graph', 'selectedData'),
        Input('line_graph', 'relayoutData'),
        Input("month_day_heat", "clickData"),
        Input("day_hour_heat", "clickData")
    ]
)
def update_dashboard(point, points, selected_data, relayout_data, month_cd, day_cd):
    global dff
    ctx = dash.callback_context
    id = ''
    if ctx.triggered:
        id = ctx.triggered[0]['prop_id'].split('.')[0]

    if point is None and points is None and selected_data is None and (relayout_data is None or x0 not in relayout_data) and month_cd is None and day_cd is None:
       raise dash.exceptions.PreventUpdate

    if id == 'md_map' and points != None and 'points' in points:
        cbmls = [point['location'] for point in points['points'] if 'location' in point ]
        dff =dff[dff.Cbml.isin(cbmls)]
    elif id == 'md_map' and point != None and 'points' in point and len(point['points']) == 1 and 'location' in point['points'][0]:
        cbml = point['points'][0]['location']
        if dff[dff.Cbml != cbml].empty:
            dff = df
        else :
            dff = dff[dff.Cbml==cbml]
    elif id == 'line_graph' and relayout_data != None and x0 in relayout_data:
        dff=dff[(dff.Date >= relayout_data[x0]) & (dff.Date <= relayout_data[x1])]
    elif id == 'line_graph' and selected_data != None and 'range' in selected_data and 'x' in selected_data['range']:
        dff=dff[(dff.Date >= selected_data['range']['x'][0]) & (dff.Date <= selected_data['range']['x'][1])]
    elif id == 'month_day_heat' and month_cd != None and 'points' in month_cd and len(month_cd['points']) == 1 and 'x' in month_cd['points'][0] and 'y' in month_cd['points'][0]:
        month = months[month_cd['points'][0]['x']]
        if dff[(dff['Date'].dt.month != month)].empty:
            dff = dff[(dff['Date'].dt.month.isin(months.values))]
        dff = dff[(dff['Date'].dt.month == month)]
    elif id == 'day_hour_heat' and day_cd != None and 'points' in day_cd and len(day_cd['points']) == 1 and 'x' in day_cd['points'][0] and 'y' in day_cd['points'][0]:
        dayofweek = order_days[day_cd['points'][0]['x']]
        if dff[(dff['Date'].dt.dayofweek != dayofweek)].empty:
            dff = dff[(dff['Date'].dt.month.isin(order_days.values))]
        dff = dff[(dff['Date'].dt.dayofweek == dayofweek)]
    else :
        dff = df    

    map_md = md_map.update_map(dff)
    month_day_heat = heat_maps.update_month_day_heat(dff)
    day_hour_heat = heat_maps.update_day_hour_heat(dff)
    line_graph = heat_maps.update_line_graph(dff)   
    return [map_md,month_day_heat,day_hour_heat,line_graph]



if __name__ == "__main__":
    # http_server = WSGIServer(('', 8080), app.server)
    # http_server.serve_forever()
    app.run_server()
    #use the bottom option when debbuging
    #app.run_server(host='localhost',port='8050',debug=True,use_reloader=True)
