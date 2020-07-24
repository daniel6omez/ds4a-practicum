import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from modules import md_map, heat_maps, prediction_widget, regression_pred

def modal_for_prediction():
    modal = html.Div([
                #dbc.Button("Open modal", id="open"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Drive carefully:"),                        
                        dbc.ModalBody("Here is the prediction", id="modal_text"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                        ),
                    ],
                    id="modal",
                ),
            ], style={'float':'right'})

    return modal


main_layout =html.Div(
[ 
    dcc.Loading(
    [        
        dbc.Row([
            dbc.Col(
                html.H5("Select a date to predict"),align="center"
            )
        ],align="center"),
        dbc.Row([
            dbc.Col(
                prediction_widget.date_picker_model,align="center"
            )
        ],align="center"),
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
        ]),
        modal_for_prediction()
            
    ],fullscreen=True)
])