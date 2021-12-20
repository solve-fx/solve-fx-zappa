import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date
#import awswrangler as wr

#df = wr.s3.read_csv('s3://bucket-fxdata/gbpjpy_last100.csv')

### Average Candle ###
def create_avgcandle(flask_app):
    dash_app = dash.Dash(server = flask_app, name = "Dashboard", url_base_pathname="/dash/")
    #dash_app.config.update({'requests_pathname_prefix': '/dev/'})

    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }
    dash_app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(children='Dash: A web application framework for Python.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
    ])

    return dash_app

