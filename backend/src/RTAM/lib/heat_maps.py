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

from sqlalchemy import create_engine
 
DB_USERNAME = 'postgres@psql-ds4a-prod'
DB_PASSWORD = 'FliFUDlbO72cq2h9AaFF'
HOST = 'psql-ds4a-prod.postgres.database.azure.com'

#engine = create_engine('sqlite:///crime.db')
engine=create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{HOST}/ds4a', max_overflow=20)
df = pd.read_sql("select * from processed.accidents", engine.connect(), parse_dates=('Date'))

#df = pd.read_csv("Data/accidents_v3.csv", parse_dates=['Date'])

def update_month_day_heat(start_date= None, end_date= None):
    dff=df
    if start_date != None and end_date != None:
        dff=df[(df.Date >= start_date) & (df.Date <= end_date)]
        
    pivot_day_month = dff.pivot_table(index='WeekDay',columns='Month', values="Radicado", aggfunc=lambda x: x.count())
    pivot_day_month = pivot_day_month.reset_index()
    pivot_day_month["WeekDay"] = pivot_day_month["WeekDay"].str.strip()

    pivot_day_month['WeekDay'] = pivot_day_month['WeekDay'].map({'Monday':'0Monday', 'Tuesday':'1Tuesday', 'Wednesday':'2Wednesday', 'Thursday':'3Thursday', 'Friday':'4Friday', 'Saturday':'5Saturday', 'Sunday':'6Sunday'})
    
    pivot_day_month.sort_values(by="WeekDay", inplace=True)
    pivot_day_month.set_index("WeekDay", inplace=True)
    pivot_day_month
    figure4 = px.imshow(pivot_day_month,
                color_continuous_scale='RdBu_r',
                labels=dict(x="Months", y="Day of Week", color="Accidents"),#"Productivity"),
                x=["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"],
                y=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
               )
    figure4.update_xaxes(side="top")
    figure4.update_layout(
    #title='GitHub commits per day',
    yaxis_nticks=24)
    
    return figure4

#######################################

def update_day_hour_heat(start_date= None, end_date= None):
    dff=df
    if start_date != None and end_date != None:
        dff=df[(df.Date >= start_date) & (df.Date <= end_date)]
        
    pivot_hours_day = dff.pivot_table(index='Hour',columns='WeekDay', values="Radicado", aggfunc=lambda x: x.count())
    map_list = {'Monday':'0Monday', 'Tuesday':'1Tuesday', 'Wednesday':'2Wednesday', 'Thursday':'3Thursday', 'Friday':'4Friday', 'Saturday':'5Saturday', 'Sunday':'6Sunday'}
    pivot_hours_day.columns = [map_list[c.strip()] for c in pivot_hours_day.columns]
    pivot_hours_day.sort_index(axis=1, inplace=True)

    figure5 = px.imshow(pivot_hours_day,
                color_continuous_scale='RdBu_r',#'RdBu_r',
                labels=dict(x="Day", y="Hour", color="Accidents"),#"Productivity"),
                x=pivot_hours_day.columns,
                y=pivot_hours_day.index
               )
    figure5.update_xaxes(side="top")
    figure5.update_layout(
    #title='GitHub commits per day',
    yaxis_nticks=24)
    
    return figure5

def update_line_graph(start_date= None, end_date= None):
    dff=df
    if start_date != None and end_date != None:
        dff=df[(df.Date >= start_date) & (df.Date <= end_date)]
        
    dff = dff.set_index("Date")
    df1 = dff.groupby([pd.Grouper(freq="M")])['Radicado'].count().reset_index()
    figure1 = px.line(df1, x="Date", y="Radicado")
    return figure1


##############################################################
# SCATTER PLOT
###############################################################

#Scatter_fig=px.scatter(df, x="Sales", y="Profit", color="Category", hover_data=['State','Sub-Category','Order ID','Product Name'])  
#Scatter_fig.update_layout(title='Sales vs. Profit in selected states',paper_bgcolor="#F8F9F9")


###############################################################
# LINE PLOT
###############################################################

#df['Order_Month'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))

#Next, we filter the data by month and selected states
#states=['California', 'Texas','New York']

#ddf=df[df['State'].isin(states)]
#ddf=ddf.groupby(['State','Order_Month']).sum().reset_index()

#Line_fig=px.line(ddf,x="Order_Month",y="Sales", color="State")
#Line_fig.update_layout(title='Montly Sales in selected states',paper_bgcolor="#F8F9F9")


#Treemap_fig=px.treemap(df, path=["Category","Sub-Category","State"],values="Sales",color_discrete_sequence=px.colors.qualitative.Dark24)

#################################################################################
# Here the layout for the plots to use.
#################################################################################
heatmaps=html.Div([ 
	#Place the different graph components here.
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=update_month_day_heat(), id='MonthDayHeat')
        ),
        dbc.Col(
            dcc.Graph(figure=update_day_hour_heat(), id='DayHourHeat')
            )
        
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=update_line_graph(),id='LineGraph')
        )
    ])
	],className="ds4a-body")



