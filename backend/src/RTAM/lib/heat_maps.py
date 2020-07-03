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

df = pd.read_csv("Data/accidents_cleanV2.csv", parse_dates=['fecha_incidente'])

def update_month_day_heat(start_date= None, end_date= None):
    dff=df
    if start_date != None and end_date != None:
        dff=df[(df.fecha_incidente >= start_date) & (df.fecha_incidente <= end_date)]
        
    pivot_day_month = dff.pivot_table(index='dia_nombre',columns='mes', values="radicado", aggfunc=lambda x: x.count())
    pivot_day_month = pivot_day_month.reset_index()
    pivot_day_month["dia_nombre"] = pivot_day_month["dia_nombre"].str.strip()
    
    pivot_day_month['dia_nombre'] = pivot_day_month['dia_nombre'].map({'LUNES':'0LUNES', 'MARTES':'1MARTES', 'MIÉRCOLES':'2MIÉRCOLES', 'JUEVES':'3JUEVES', 'VIERNES':'4VIERNES', 'SÁBADO':'5SÁBADO', 'DOMINGO':'6DOMINGO'})
    
    pivot_day_month.sort_values(by="dia_nombre", inplace=True)
    pivot_day_month.set_index("dia_nombre", inplace=True)
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
    yaxis_nticks=24, width=1200)
    
    return figure4

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
        )#,
        #dbc.Col(
         #   dcc.Graph(figure=Scatter_fig, id='Scatter')
          #  )
        
    ])#,
   # dbc.Row([
    #    dbc.Col(
     #   dcc.Graph(figure=Treemap_fig,id='Treemap')
      #  )
   # ])
	],className="ds4a-body")



