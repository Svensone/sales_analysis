import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_dangerously_set_inner_html

import dash_html_components as html
from utils import Header

import pandas as pd


def create_layout(app, df):
    img_test = app.get_asset_url('bg.jpg')
    html_test = app.get_asset_url('plotly_fb_test.html')
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # IFrame Row
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(['Sales Forecasting'],
                                            className="subtitle padded"
                                            ),
                                    html.H6(['Comparing Facebook Prophet - Tableau - Neuronal Network Pytorch'],
                                            className="disclaimer padded"
                                            ),
                                ]
                            )
                        ],
                        className="row ",
                    ),
                    # IFrame Row
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(['Sales Prediction Fb Prophet - 7 days'],
                                            className="disclaimer padded"),
                                    html.Iframe(
                                        src=html_test,
                                        height=650,
                                        width=920,
                                        style={'border': 'none'}
                                    )
                                ]
                            )
                        ],
                        className="row ",
                    ),
                    # JSON File from Colab Notebook
                    html.Div(
                        [
                            html.Div(
                                [

                                    html.H6(
                                        ['Prophet Components Analysis Graph'],
                                        className="disclaimer padded"
                                    ),
                                    # with callback
                                    html.Button(
                                        "Click me", id='prophet_components_input'),
                                    dcc.Graph(id='prophet_components'),
                                ],
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
