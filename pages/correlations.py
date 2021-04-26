import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

# from dash.dependencies import Input, Output
# from app import app

import pathlib

##############################################################
#  to-dos:
#
# https://plotly.com/python/heatmaps/
# heatmapz - create in Colab and import as html

##############################################################

# from heatmap import heatmap,     0\ corrplot
from html_blocks import get_disclaimer_block, get_image_block
from utils import Header, make_dash_table

import pandas as pd


def create_layout(app, df):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    #################
                    # Row Correlation Matrix - Plotly
                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Pearson Correlations Matrix"],
                                            className="subtitle padded"),
                                    html.Br(),
                                    html.Div([
                                        dcc.Dropdown(
                                            id='corr_selector',
                                            options=[
                                                {"label": "Storetype 'A",
                                                    "value": 'a'},
                                                {"label": "Storetype 'B",
                                                    "value": 'b'},
                                            ],
                                            value='a',
                                            clearable=False,
                                        ),
                                        dcc.Graph(
                                            id='corr_matrix',
                                        ),
                                    ])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    #################
                    # Row Correlation Matrix - Seaborn
                    ################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Correlations Matrix - Seaborn"],
                                            className="subtitle padded"),
                                    html.Br(),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    ##########
                    # Row Monthly Sales and Promotion
                    ##########
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Monthly Sales - Storetype and Promotion1"], className="subtitle"),
                                    html.Br([]),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
