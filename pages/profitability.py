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
    # SpC Overview Analysis (Bar Total, Line (rolling ave. & LIne pct_change))
    # ######################
    #  selector for Storetype
    
    return html.Div(
        [
            Header(app),
            # page 3
            html.Div(
                [
                    ################
                    # Profitability Analysis
                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(['Profitability'],
                                            className='subtitle padded'),
                                    html.Div([
                                        ])
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
                            html.H6(['Outlier Analysis'],
                                    className='subtitle padded'),
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