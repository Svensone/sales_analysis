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

# COLOR_VAR
color_extralight = 'rgb(247,251,255)'
color_bg = 'rgb(222,235,247)'
color_main = 'rgb(33,113,181)'
color_dark = 'rgb(8,48,107)'


def create_layout(app, df):
    # SpC Overview Analysis (Bar Total, Line (rolling ave. & LIne pct_change))
    # ######################
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

#
    # python app.py
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
                    #
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
                    # Disclaimer row
                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Disclamer : "],
                                        className="disclaimer padded"),
                                    html.Strong(
                                        "More Time Series Analysis in Notebook, see::"),
                                    html.Br(),
                                    html.A(
                                        html.Button(
                                            "Github", className="disclaimer_button"),
                                        href="https://github.com/Svensone/kaggle/blob/main/Competitions/Sales_Performance_Analysis_%26_Prediction_Rossmann.ipynb",
                                        target='_blank',
                                    ),
                                ],
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

    #     html.H6(['Day of Week Sales-Analysis'],
    #             className='subtitle padded'),
    #     html.Div([
    #         html.H6(['Sales'], className='padded'),
    #         html.Br(),
    #         html.Div([
    #             dcc.Dropdown(
    #                 id='weekDay_sales_selector',
    #                 options=[
    #                     {"label": "Storetype 'A", "value": 'a'},
    #                     {"label": "Storetype 'B", "value": 'b'},
    #                     {"label": "Storetype 'C", "value": 'c'},
    #                     {"label": "Storetype 'D", "value": 'd'},
    #                 ],
    #                 value='a',
    #                 clearable=False,
    #             ),
    #             dcc.Graph(
    #                 id='weekDay_sales',
    #                 figure=fig_weekDay_sales,),
    #                 ]),
    #             ],
    #         ),
    #     html.Div([
    #         html.H6(['Customers'], className='padded'),
    #         html.Br(),
    #         dcc.Graph(
    #             id='weekDay_customer',
    #             figure=fig_weekDay_customer,),
    #         ]
    #         ),
    #     ], className='six columns'
    #     ),
    # ],
    #     className='row'
    # ),
