import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

from utils import Header, make_dash_table
from html_blocks import get_image_block

import pandas as pd
import pathlib

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from variables import color_extralight, color_bg, color_light, color_main_light, color_main, color_dark_light, color_dark, color_transparent, color_contr, color_contr2


def create_layout(app, df):
    #  selector for Storetype
    # Week Day Analysis (Bar plot)
    # ######################
    fig_weekDay_sales = px.bar(df, x='DayOfWeek', y='Sales')
    # fig_weekDay_sales.update_traces(color=color_dark)
    fig_weekDay_sales.update_layout(
        paper_bgcolor='rgb(0,0,0,0)', hovermode="closest", plot_bgcolor='rgb(0,0,0,0)')
    fig_weekDay_customer = px.bar(df, x='DayOfWeek', y='Customers')
    # fig_weekDay_customer.update_traces(color=color_dark)
    fig_weekDay_customer.update_layout(
        paper_bgcolor='rgb(0,0,0,0)', hovermode="closest", plot_bgcolor='rgb(0,0,0,0)')

    return html.Div(
        [
            Header(app),
            # page 3
            html.Div(
                [
                    ################
                    # Seasonality Analysis
                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(['Seasonality'],
                                            className='subtitle padded'),
                                    html.Div([
                                        dcc.Dropdown(
                                            id='seasonality_selector',
                                            options=[
                                                {"label": "Storetype 'A",
                                                    "value": 'a'},
                                                {"label": "Storetype 'B",
                                                    "value": 'b'},
                                                {"label": "Storetype 'C",
                                                    "value": 'c'},
                                                {"label": "Storetype 'D",
                                                    "value": 'd'},
                                            ],
                                            value='a',
                                            clearable=False,
                                        ),
                                        dcc.Graph(
                                            id='seasonality_graph',
                                        )])
                                ],
                            )
                        ],
                        className="row ",
                    ),
                    ################
                    # Week Days Analysis
                    ################
                    html.Div([
                    ],
                        className='row'
                    ),
                    ################
                    # Stationarity
                    ################
                    html.Div([
                        html.Div([
                            html.H6(['Analysis'],
                                    className='disclaimer padded'),
                                ]
                                ),
                            ],
                        className='row'
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )