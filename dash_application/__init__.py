import dash
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import html

#import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date
import boto3
import pandas as pd

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-2'
)

obj = s3.Bucket('bucket-fxdata').Object('gbpjpy_last100.csv').get()
df = pd.read_csv(obj['Body'], index_col=0)

max_date = df.index.max()

### Average Candle ###
def create_avgcandle(flask_app):
    dash_app = dash.Dash(server = flask_app, name = "Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Card components
    cards = [
        dbc.Card(
            [
                html.P("Earliest Date:", className="card-text"),
                html.H2(id='my-output', className="card-title")
            ],
            body=True,
            color="dark",
            inverse=True
        ),
        dbc.Card(
            [
                html.P("Latest Date:", className="card-text"),
                html.H2(str(max_date)+" UTC", className="card-title"),
            ],
            body=True,
            color="dark",
            inverse=True
        )
    ]

    # Selectors & Labels - Timeframe & Pair
    selector_labels = [
            html.P("Select Timeframe"),
            html.P("Select Pair"),
        ]

    selectors = [
        dcc.RadioItems(
            id = 'timeframe-buttons',
            options=[
            {'label': '5m', 'value': '5m'},
            {'label': '15m', 'value': '15m'},
            {'label': '30m', 'value': '30m'},
            {'label': '1h', 'value': '1h'},
            {'label': '4h', 'value': '4h'},
            ],
            value='30m'
        ),
        dcc.RadioItems(
            id = 'pairs-buttons',
            options=[
            {'label': 'GBP/JPY', 'value': 'GBP/JPY'},
            ],
            value='GBP/JPY'
        )
    ]

    # Slider - number of days
    weeks = df['days_since'].unique()[df['days_since'].unique() % 7 == 0]
    week_marks = {str(days): str(days) for days in weeks}

    
    slider = dcc.Slider(
        id='year-slider',
        min=df['days_since'].min(),
        max=df['days_since'].max(),
        step = 5,
        value=15,
        marks=week_marks
    )

    #graphs
    graphs = [
        dcc.Graph(id='graph-with-slider'),
        dcc.Graph(id='graph-with-slider2')
    ]


    dash_app.layout = dbc.Container(
        [
            html.Hr(),
            dbc.Row([dbc.Col(card) for card in cards]),
            html.Br(),
            dbc.Row([dbc.Col(selector_label) for selector_label in selector_labels]),
            dbc.Row([dbc.Col(selector) for selector in selectors]),
            html.Br(),
            html.P("Select number of days"),
            dbc.Row([slider]),
            html.Br(),
            html.Div([dcc.Graph(id='graph-with-slider' )],  style={'width': '100%', 'height':'90%', 'padding': '0 20'}),
            html.Div([dcc.Graph(id='graph-with-slider2')],  style={'width': '100%', 'height':'90%', 'padding': '0 20'})
        ],
        fluid=False,
    )
    
    @dash_app.callback(
        
            Output('graph-with-slider', 'figure'),
            Output('graph-with-slider2', 'figure'),
            Output('my-output', 'children')
        ,

        
            Input('year-slider', 'value'),
            Input('timeframe-buttons', 'value')
        
    )

    def update_figure(selected_days, selected_timeframe):
        filtered_df = df[(df.days_since <= selected_days) & (df.timeframe == selected_timeframe)]

        #max_date = filtered_df.index.max()
        min_date = str(filtered_df.index.min()) + " UTC"
        
        table = pd.pivot_table(filtered_df, values='candle_size', index=['time'], aggfunc=np.mean) 
        table['time'] = table.index
        fig = px.bar(table, x='time', y='candle_size', title = 'Average candle movement of last x days')
        fig.update_layout(transition_duration=500)

        table = pd.pivot_table(filtered_df, values='bullish', index=['time'], aggfunc=np.mean) 
        table['time'] = table.index
        fig2 = px.bar(table, x='time', y='bullish', title = 'Proportion of candles bullish last x days')
        fig2.update_layout(transition_duration=500)

        return fig, fig2, min_date
                

    return dash_app

