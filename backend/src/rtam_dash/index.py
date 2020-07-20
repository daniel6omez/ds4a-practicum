import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server

from layouts import main_layout
import callbacks

app.layout = main_layout

if __name__ == "__main__":
    app.run_server()
