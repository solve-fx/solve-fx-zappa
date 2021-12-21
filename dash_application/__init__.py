import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date
import boto3
import pandas as pd

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-2'#,
    #aws_access_key_id='',
    #aws_secret_access_key=''
)

obj = s3.Bucket('bucket-fxdata').Object('gbpjpy_last100.csv').get()
df = pd.read_csv(obj['Body'], index_col=0)

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

