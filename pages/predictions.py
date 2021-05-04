import dash
import dash_core_components as dcc
import dash_html_components as html

from utils import Header
import pandas as pd

def create_layout(app, df):
    html_test = app.get_asset_url('plotly_fb_test.html')
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # Row
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(['Sales Forecasting'],
                                            className="subtitle padded"
                                            ),
                                    html.Br(),
                                    html.Br(),
                                    html.H6(['Comparing Facebook Prophet - Tableau - Neuronal Network Pytorch'],
                                            className="subtitle padded"
                                            ),
                                    dcc.Graph(
                                        id= 'prediction_graph',
                                    ),
                                    dcc.Dropdown(
                                            id='prediction_selectors',
                                            options=[
                                                {"label": "FB-Prophet", "value": 'prophet'},
                                                {"label": "FastAI Neural Net", "value": 'fastai'},
                                                {"label": "Tableau", "value": 'tableau'},
                                                {"label": "Power BI", "value": 'powerBI'},
                                            ],
                                            value='prophet',
                                            clearable=False,
                                        ),
                                ]
                            )
                        ],
                        className="row ",
                    ),
                    # Row Prophet Time Series (IFrame)
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(['Sales Prediction Fb Prophet - 7 days'],
                                            className="subtitle padded"),
                                    html.Iframe(
                                        src=html_test,
                                        height=500,
                                        width=920,
                                        style={'border': 'none'}
                                    )
                                ]
                            )
                        ],
                        className="row ",
                    ),
                    # Row Prophet Components (JSON File from Colab Notebook)
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ['Prophet Components Analysis Graph'],
                                        className="subtitle padded"
                                    ),
                                    dcc.Graph(id='prophet_components'),
                                    dcc.RadioItems(
                                        id='prophet_components_input',
                                        options=[
                                            {'label': 'Component', 'value': 'week'}
                                            ],
                                        value='week'),
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
