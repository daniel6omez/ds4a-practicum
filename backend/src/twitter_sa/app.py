import settings # Import related setting constants from settings.py 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import settings
import itertools
import math
import base64
from flask import Flask
import os
from sqlalchemy import create_engine
import datetime
from googletrans import Translator  
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

today = datetime.datetime.now().strftime("%B %d, %Y")
translator = Translator()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.title = 'Real-Time Twitter Monitor'

app.layout = html.Div(children=[
    #html.H2('Real-time Twitter Sentiment Analysis for Topic Tracking', style={'textAlign': 'center'}),
    html.P('(Last updated: {})'.format(today), style={'textAlign': 'right', 'fontSize':15}),
    
    html.Div(id='live-update-graph'),
    html.Div(id='live-update-graph-bottom'),
    
    # ABOUT ROW
    html.Div(
        className='row',
        children=[
            html.Div(
                className='three columns',
                children=[
                    html.P(
                    'Data extracted from:'
                    ),
                    html.A(
                        'Twitter API',
                        href='https://developer.twitter.com'
                    )                    
                ]
            ),
            html.Div(
                className='three columns',
                children=[
                    html.P(
                    'Code avaliable at:'
                    ),
                    html.A(
                        'GitHub',
                        href='https://github.com/Chulong-Li/Real-time-Sentiment-Tracking-on-Twitter-for-Brand-Improvement-and-Trend-Recognition'
                    )                    
                ]
            ),
            html.Div(
                className='three columns',
                children=[
                    html.P(
                    'Made with:'
                    ),
                    html.A(
                        'Dash / Plot.ly',
                        href='https://plot.ly/dash/'
                    )                    
                ]
            ),
            html.Div(
                className='three columns',
                children=[
                    html.P(
                    'Author:'
                    ),
                    html.A(
                        'Chulong Li',
                        href='https://www.linkedin.com/in/chulong-li/'
                    )                    
                ]
            )                                                          
        ], style={'marginLeft': 70, 'fontSize': 8}
    ),

    dcc.Interval(
        id='interval-component-slow',
        interval=1*10000, # in milliseconds
        n_intervals=0
    )
    ], style={'padding': '20px'})



# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'children'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_live(n):
    # Loading data from RDS PostgreSQL
    engine = create_engine('postgresql://postgres@psql-ds4a-prod:FliFUDlbO72cq2h9AaFF@psql-ds4a-prod.postgres.database.azure.com:5432/ds4a_mta_twitterdb')
    query = "SELECT id_str, text, created_at, polarity, user_location, user_followers_count FROM {}".format(settings.TABLE_NAME)
    df = pd.read_sql(query,engine)
    # Convert UTC into PDT
    df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x - datetime.timedelta(hours=3))

    # Clean and transform data to enable time series
    result = df.groupby([pd.Grouper(key='created_at', freq='10s'), 'polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"id_str": "Num of '{}' mentions".format(settings.TRACK_WORDS[0]), "created_at":"Time"})  
    time_series = result["Time"][result['polarity']==0].reset_index(drop=True)

    min10 = datetime.datetime.now() - datetime.timedelta(hours=3, minutes=10)
    min20 = datetime.datetime.now() - datetime.timedelta(hours=3, minutes=20)

    neu_num = result[result['Time']>min10]["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==0].sum()
    neg_num = result[result['Time']>min10]["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==-1].sum()
    pos_num = result[result['Time']>min10]["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==1].sum()
    
    # Loading back-up summary data
    # This table must be create before 
    query = "SELECT daily_user_num, daily_tweets_num, impressions FROM backup;"
    back_up = pd.read_sql(query, engine)  
    daily_tweets_num = back_up['daily_tweets_num'].iloc[0] + result[-6:-3]["Num of '{}' mentions".format(settings.TRACK_WORDS[0])].sum()
    daily_impressions = back_up['impressions'].iloc[0] + df[df['created_at'] > (datetime.datetime.now() - datetime.timedelta(hours=7, seconds=10))]['user_followers_count'].sum()
    engine.connect()
    mydb = engine.raw_connection()
    mycursor = mydb.cursor()

    PDT_now = datetime.datetime.now() - datetime.timedelta(hours=3)
    if PDT_now.strftime("%H%M")=='0000':
        mycursor.execute("UPDATE backup SET daily_tweets_num = 0, impressions = 0;")
    else:
        mycursor.execute("UPDATE backup SET daily_tweets_num = {}, impressions = {};".format(daily_tweets_num, daily_impressions))
    mydb.commit()
    mycursor.close()
    mydb.close()

    # Percentage Number of Tweets changed in Last 10 mins
    count_now = df[df['created_at'] > min10]['id_str'].count()
    count_before = df[ (min20 < df['created_at']) & (df['created_at'] < min10)]['id_str'].count()

    if count_before == 0:
        count_before = 24000

    percent = (count_now-count_before)/count_before*100

    # Create the graph backup
    print("Percent: ", percent)
    children = [
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='crossfilter-indicator-scatter',
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=time_series,
                                        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==0].reset_index(drop=True),
                                        name="Neutrals",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(165, 166, 164)'),
                                        stackgroup='one' 
                                    ),
                                    go.Scatter(
                                        x=time_series,
                                        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==-1].reset_index(drop=True).apply(lambda x: -x),
                                        name="Negatives",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(252, 149, 5)'),
                                        stackgroup='two' 
                                    ),
                                    go.Scatter(
                                        x=time_series,
                                        y=result["Num of '{}' mentions".format(settings.TRACK_WORDS[0])][result['polarity']==1].reset_index(drop=True),
                                        name="Positives",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(169, 245, 108)'),
                                        stackgroup='three' 
                                    )
                                ]
                            }
                        )
                    ], style={'width': '73%', 'display': 'inline-block', 'padding': '0 0 0 20'}),
                    
                    html.Div([
                        dcc.Graph(
                            id='pie-chart',
                            figure={
                                'data': [
                                    go.Pie(
                                        labels=['Positives', 'Negatives', 'Neutrals'], 
                                        values=[pos_num, neg_num, neu_num],
                                        name="View Metrics",
                                        marker_colors=['rgba(169, 245, 108, 0.6)','rgba(252, 149, 5, 0.6)','rgba(165, 166, 164, 0.6)'],
                                        textinfo='value',
                                        hole=.65)
                                ],
                                'layout':{
                                    'showlegend':False,
                                    'title':'Tweets In Last 10 Mins',
                                    'annotations':[
                                        dict(
                                            text='{0:.1f}'.format((pos_num+neg_num+neu_num)),
                                            font=dict(
                                                size=17
                                            ),
                                            showarrow=False
                                        )
                                    ]
                                }

                            }
                        )
                    ], style={'width': '27%', 'display': 'inline-block'})
                ]),
                
                html.Div(
                    className='row',
                    children=[
                        html.Div(
                            children=[
                                    #html.A('(Last updated: {})'.format(today), style={'textAlign': 'right'}),
				    html.P('Tweets/10 Mins Changed By',
                                    style={
                                        'fontSize': 17
                                    }
                                ),
                                html.P('{0:.2f}%'.format(percent) if percent <= 0 else '+{0:.2f}%'.format(percent),
                                    style={
                                        'fontSize': 40
                                    }
                                )
                            ], 
                            style={
                                'width': '20%', 
                                'display': 'inline-block'
                            }

                        ),
                        html.Div(
                            children=[
                                html.P('Potential Impressions Today',
                                    style={
                                        'fontSize': 17
                                    }
                                ),
                                html.P('{0:.1f}K'.format(daily_impressions/1000) \
                                        if daily_impressions < 1000000 else \
                                            ('{0:.1f}M'.format(daily_impressions/1000000) if daily_impressions < 10000000000 \
                                            else '{0:.1f}M'.format(daily_impressions/10000000000)),
                                    style={
                                        'fontSize': 40
                                    }
                                )
                            ], 
                            style={
                                'width': '20%', 
                                'display': 'inline-block'
                            }
                        ),
                        html.Div(
                            children=[
                                html.P('Tweets Posted Today',
                                    style={
                                        'fontSize': 17
                                    }
                                ),
                                html.P('{0:.1f}K'.format(daily_tweets_num/1000),
                                    style={
                                        'fontSize': 40
                                    }
                                )
                            ], 
                            style={
                                'width': '20%', 
                                'display': 'inline-block'
                            }
                        ),

                        html.Div(
                            children=[
                                html.P("Currently tracking Movilidad Medellín on Twitter in Pacific Daylight Time (PDT).",
                                    style={
                                        'fontSize': 15
                                    }
                                ),
                            ], 
                            style={
                                'width': '40%', 
                                'display': 'inline-block'
                            }
                        ),

                    ],
                    style={'marginLeft': 70}
                )
            ]
    return children


@app.callback(Output('live-update-graph-bottom', 'children'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_bottom_live(n):

    # Loading data from RDS PostgreSQL
    engine = create_engine('postgresql://postgres@psql-ds4a-prod:FliFUDlbO72cq2h9AaFF@psql-ds4a-prod.postgres.database.azure.com:5432/ds4a_mta_twitterdb')
    query = "SELECT id_str, text, created_at, polarity, user_location FROM {}".format(settings.TABLE_NAME)
    df = pd.read_sql(query, engine)

    # Convert UTC into PDT
    df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x - datetime.timedelta(hours=1))

    # Clean and transform data to enable word frequency
    content = ' '.join(df["text"])
    content = re.sub(r"http\S+", "", content)
    content = content.replace('RT ', ' ').replace('&amp;', 'and')
    content = re.sub('[^A-Za-z0-9]+', ' ', content)
    content = content.lower()
    
    dic_word_to_remove = ['cadenagaitan', 'quinterocalle', 'personeriamed', 'alcaldiademed', 'emvarias', 'medelln' ]
    for  i in dic_word_to_remove:
          content = re.sub(i, ' ', content)
    

    #content = Translator(content)
    # Filter constants for states in US
  
    tokenized_word = word_tokenize(content)
    stop_words=set(stopwords.words("spanish"))
    filtered_sent=[]
    for w in tokenized_word:
        if (w not in stop_words) and (len(w) >= 4):
            filtered_sent.append(w)
    fdist = FreqDist(filtered_sent)
    fd = pd.DataFrame(fdist.most_common(20), columns = ["Word","Frequency"]).drop([0]).reindex()
   
    fd['Polarity2'] = fd['Word'].apply(lambda x: translator.translate(x, src='es', dest='en').text)
    fd['Polarity'] = fd['Polarity2'].apply(lambda x: TextBlob(x).sentiment.polarity)
    #fd = fd[fd.Polarity != 0]

    fd['Marker_Color'] = fd['Polarity'].apply(lambda x: 'rgba(165, 166, 164, 0.6)' if x < -0.1 else \
        ('rgba(184, 247, 212, 0.6)' if x > 0.1 else 'rgba(169, 245, 108, 0.6)'))
    

    fd['Line_Color'] = fd['Polarity'].apply(lambda x: 'rgba(165, 166, 164, 1)' if x < -0.1 else \
        ('rgba(184, 247, 212, 1)' if x > 0.1 else 'rgba(169, 245, 108, 1)'))



    # Create the graph 
    children = [
                html.Div([
                    dcc.Graph(
                        id='x-time-series',
                        figure = {
                            'data':[
                                go.Bar(                          
                                    x=fd["Frequency"].loc[::-1],
                                    y=fd["Word"].loc[::-1], 
                                    name="Neutrals", 
                                    orientation='h',
                                    marker_color=fd['Marker_Color'].loc[::-1].to_list(),
                                    marker=dict(
                                        line=dict(
                                            color=fd['Line_Color'].loc[::-1].to_list(),
                                            width=1),
                                        ),
                                )
                            ],
                            'layout':{
                                'hovermode':"closest"
                            }
                        }        
                    )
                ], style={'width': '100%', 'display': 'inline-block', 'padding': '50 50 50 50'}),
                html.Div([
                    
                ], style={'display': 'inline-block', 'width': '100%'})
            ]
        
    return children


if __name__ == '__main__':
    app.run_server(debug=True,port=8051, host='127.0.0.1')
