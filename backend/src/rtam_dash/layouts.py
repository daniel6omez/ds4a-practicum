import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from modules import md_map, heat_maps

main_layout =html.Div(
[ 
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=md_map.update_map(), id='md_map'),xl=6, lg=6, md=6, xs=12
        ),
        dbc.Col(
            dcc.Graph(figure=heat_maps.update_line_graph(),id='line_graph'),xl=6, lg=6, md=6, xs=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=heat_maps.update_month_day_heat(), id='month_day_heat'),xl=6, lg=6, md=6, xs=12
        ),
        dbc.Col(
            dcc.Graph(figure=heat_maps.update_day_hour_heat(), id='day_hour_heat'),xl=6, lg=6, md=6, xs=12
            )
    ])
])
