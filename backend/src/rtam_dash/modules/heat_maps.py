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
    figure4.update_layout(yaxis_nticks=24,margin=dict(l=10, r=10, t=10, b=10))
    
    return figure4

#######################################

def update_day_hour_heat(dff = df):
    pivot_hours_day = dff.pivot_table(index='WeekDay',columns='Hour', values="Radicado", aggfunc=lambda x: x.count())
    pivot_hours_day = pivot_hours_day.reset_index()
    pivot_hours_day["WeekDay"] = pivot_hours_day["WeekDay"].str.strip()

    pivot_hours_day['WeekDay'] = pivot_hours_day['WeekDay'].map({'Monday':'0Monday', 'Tuesday':'1Tuesday', 'Wednesday':'2Wednesday', 'Thursday':'3Thursday', 'Friday':'4Friday', 'Saturday':'5Saturday', 'Sunday':'6Sunday'})
    
    pivot_hours_day.sort_values(by="WeekDay", inplace=True)
    pivot_hours_day.set_index("WeekDay", inplace=True)

    figure5 = px.imshow(pivot_hours_day,
                color_continuous_scale='RdBu_r',
                labels=dict(x="Hour", y="Day", color="Accidents"),
                x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
                y=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
               )
    figure5.update_xaxes(side="top")
    figure5.update_layout(xaxis_nticks=24,margin=dict(l=10, r=10, t=10, b=10))
    
    return figure5

def update_line_graph(dff = df):
        
    df1 = dff.set_index("Date").groupby([pd.Grouper(freq="M")])['Radicado'].count().reset_index()
    # figure1 = px.line(df1, x='Date', y='Radicado')
    # figure1.update_traces(mode='lines+markers')
    fig = go.Figure(data=go.Scatter(x=df1.Date, y=df1.Radicado, mode='lines+markers',customdata=df.index))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    return fig

#################################################################################
# Here the layout for the plots to use.
#################################################################################
heatmaps=html.Div([ 
	#Place the different graph components here.
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=update_month_day_heat(), id='month_day_heat',style={'height':'35vh'})
        ),
        dbc.Col(
            dcc.Graph(figure=update_day_hour_heat(), id='day_hour_heat',style={'height':'35vh'})
            )
        
    ]),
    dcc.Graph(figure=update_line_graph(),id='line_graph',style={'height':'35vh'}),
    
   
	])



