#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization. 
#######################################################




import dash
import dash_bootstrap_components as dbc 


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP],meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'DS4A',
        'content': 'RTAM'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }
])
server = app.server

#We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True




