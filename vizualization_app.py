# from scripts import MainData

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table


import requests
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as poi


# data_object = MainData.GeneralData(seasons=[2020, 2021, 2022])
# fixture = data_object.fixture_data()


poi.renderers.default = "browser"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Test Vizualization"),
                    ]
                )
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
