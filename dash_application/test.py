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

print(df)