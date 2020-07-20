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

from db.data import df


def update_month_day_heat(dff = df):

    pivot_day_month = dff.pivot_table(index='WeekDay',columns='Month', values="Radicado", aggfunc=lambda x: x.count())
    pivot_day_month = pivot_day_month.reset_index()
    pivot_day_month["WeekDay"] = pivot_day_month["WeekDay"].str.strip()

    pivot_day_month['WeekDay'] = pivot_day_month['WeekDay'].map({'Monday':'0Monday', 'Tuesday':'1Tuesday', 'Wednesday':'2Wednesday', 'Thursday':'3Thursday', 'Friday':'4Friday', 'Saturday':'5Saturday', 'Sunday':'6Sunday'})
    
    pivot_day_month.sort_values(by="WeekDay", inplace=True)
    pivot_day_month.set_index("WeekDay", inplace=True)

    figure4 = px.imshow(pivot_day_month,
                color_continuous_scale='RdBu_r',
                labels=dict(x="Months", y="Day of Week", color="Accidents"),
                x=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"],
                y=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
               )
    figure4.update_xaxes(side="top")
    figure4.update_layout(
    yaxis_nticks=24)
    
    return figure4

#######################################

def update_day_hour_heat(dff = df):
    pivot_hours_day = dff.pivot_table(index='Hour',columns='WeekDay', values="Radicado", aggfunc=lambda x: x.count())
    map_list = {'Monday':'0Monday', 'Tuesday':'1Tuesday', 'Wednesday':'2Wednesday', 'Thursday':'3Thursday', 'Friday':'4Friday', 'Saturday':'5Saturday', 'Sunday':'6Sunday'}
    pivot_hours_day.columns = [map_list[c.strip()] for c in pivot_hours_day.columns]
    pivot_hours_day.sort_index(axis=1, inplace=True)

    figure5 = px.imshow(pivot_hours_day,
                color_continuous_scale='RdBu_r',
                labels=dict(x="Day", y="Hour", color="Accidents"),
                x=pivot_hours_day.columns,
                y=pivot_hours_day.index
               )
    figure5.update_xaxes(side="top")
    figure5.update_layout(
    yaxis_nticks=24)
    
    return figure5

def update_line_graph(dff = df):
        
    df1 = dff.set_index("Date").groupby([pd.Grouper(freq="M")])['Radicado'].count().reset_index()
    # figure1 = px.line(df1, x='Date', y='Radicado')
    # figure1.update_traces(mode='lines+markers')
    fig = go.Figure(data=go.Scatter(x=df1.Date, y=df1.Radicado, mode='lines+markers',customdata=df.index))
    return fig

#################################################################################
# Here the layout for the plots to use.
#################################################################################
heatmaps=html.Div([ 
	#Place the different graph components here.
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=update_month_day_heat(), id='month_day_heat')
        ),
        dbc.Col(
            dcc.Graph(figure=update_day_hour_heat(), id='day_hour_heat')
            )
        
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=update_line_graph(),id='line_graph')
        )
    ])
	],className="ds4a-body")



