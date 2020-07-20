import dash
import dash_bootstrap_components as dbc 


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

app.meta_tags=[
    {
        'name': 'DS4A',
        'content': 'RTAM'
    },
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }
]

server = app.server

#We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True

app.title = 'DS4A'



