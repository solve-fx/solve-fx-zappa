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

### Average Candle ###
def create_avgcandle(flask_app):
    external_stylesheets = [dbc.themes.DARKLY]
    dash_app = dash.Dash(server = flask_app, name = "Dashboard", url_base_pathname="/dash/", external_stylesheets=[external_stylesheets])

    dash_app.layout =   html.Div([

                            html.Div(
                            id="quick-stats",
                            className="row",
                            children=[
                                html.Div(
                                    id="card-1",
                                    children=[
                                        html.P("Operator ID"),
                                        daq.LEDDisplay(
                                            id="operator-led",
                                            value="2021-12-02",
                                            color="#92e0d3",
                                            backgroundColor="#1e2130",
                                            size=50,
                                        ),
                                    ],
                                ),
                            ],
                            ),

                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.Label('Select Timeframe'),
                                    ], style={'font-size': '18px'}),


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
                                )], style={'width': '49%', 'display': 'inline-block'}),

                                html.Div([
                                    html.Label('Select Pair'),
                                ], style={'font-size': '18px', 'float': 'center', 'display': 'inline-block'}),

                                html.Div([    
                                    dcc.RadioItems(
                                        id = 'pairs-buttons',
                                        options=[
                                        {'label': 'GBP/JPY', 'value': 'GBP/JPY'},
                                        ],
                                        value='GBP/JPY'
                                    )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}

                                )
                            ], style={'padding': '10px 5px'}),

                            html.Div([
                                html.Label('Days Slider - Used to filter dataset for last x days'),
                            ], style={'font-size': '18px'}),

                            html.Div([
                                dcc.Slider(
                                id='year-slider',
                                min=df['days_since'].min(),
                                max=df['days_since'].max(),
                                step = 1,
                                value=15,
                                marks={str(days): str(days) for days in df['days_since'].unique()}
                                )
                            ]),

                            html.Div([
                                dcc.Graph(id='graph-with-slider'),
                            ],  style={'width': '100%', 'height':'90%', 'display': 'inline-block', 'padding': '0 20'}),

                            html.Div([
                                dcc.Graph(id='graph-with-slider2'),
                            ],  style={'width': '100%', 'height':'90%', 'display': 'inline-block', 'padding': '0 20'})
                        ])

    @dash_app.callback(
        Output('graph-with-slider', 'figure'),
        Output('graph-with-slider2', 'figure'),
        Input('year-slider', 'value'),
        Input('timeframe-buttons', 'value'))


    def update_figure(selected_days, selected_timeframe):
        filtered_df = df[(df.days_since <= selected_days) & (df.timeframe == selected_timeframe)]
        

        table = pd.pivot_table(filtered_df, values='candle_size', index=['time'], aggfunc=np.mean) 
        table['time'] = table.index
        fig = px.bar(table, x='time', y='candle_size', title = 'Average candle movement of last x days')
        fig.update_layout(transition_duration=500)

        table = pd.pivot_table(filtered_df, values='bullish', index=['time'], aggfunc=np.mean) 
        table['time'] = table.index
        fig2 = px.bar(table, x='time', y='bullish', title = 'Proportion of candles bullish last x days')
        fig2.update_layout(transition_duration=500)


        return fig, fig2

    return dash_app

