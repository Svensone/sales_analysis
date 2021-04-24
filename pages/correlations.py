import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from dash.dependencies import Input, Output
from app import app

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
                    # Row Correlation Matrix
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
                                                {"label": "Storetype 'A", "value": 'a'},
                                                {"label": "Storetype 'B", "value": 'b'},
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
                    # Row Key Findings Correlation
                    ##########################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Key Findings: Correlations"],
                                            className="subtitle"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Strong(
                                                                ["Promotion"],
                                                                style={
                                                                    "color": "#515151"
                                                                },
                                                            )
                                                        ],
                                                        className="three columns right-aligned",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                ["not yet"],
                                                                style={
                                                                    "color": "#7a7a7a"
                                                                },
                                                            )
                                                        ],
                                                        className="nine columns",
                                                    ),
                                                ],
                                                className="row",
                                                style={
                                                    "background-color": "#f9f9f9",
                                                    "padding-top": "20px",
                                                },
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Strong(
                                                                ["Sales per Customer"],
                                                                style={
                                                                    "color": "#515151"
                                                                },
                                                            )
                                                        ],
                                                        className="three columns right-aligned",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                ["not yet"],
                                                                style={
                                                                    "color": "#7a7a7a"
                                                                },
                                                            )
                                                        ],
                                                        className="nine columns",
                                                    ),
                                                ],
                                                className="row",
                                                style={
                                                    "background-color": "#f9f9f9"},
                                            ),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Strong(
                                                                ["Promo1"],
                                                                style={
                                                                    "color": "#515151"
                                                                },
                                                            )
                                                        ],
                                                        className="three columns right-aligned",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.P(
                                                                ["None"],
                                                                style={
                                                                    "color": "#7a7a7a"
                                                                },
                                                            )
                                                        ],
                                                        className="nine columns",
                                                    ),
                                                ],
                                                className="row",
                                                style={
                                                    "background-color": "#f9f9f9"},
                                            ),
                                        ],
                                        className="fees",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        ["Promotion 1"],
                                                        style={
                                                            "color": "#515151"},
                                                    )
                                                ],
                                                className="three columns right-aligned",
                                            ),
                                            html.Div(
                                                [
                                                    html.Strong(
                                                        [
                                                            "WeekDay"
                                                        ],
                                                        style={
                                                            "color": "#515151"},
                                                    ),
                                                    html.P(
                                                        ["not yet"],
                                                        style={
                                                            "color": "#7a7a7a"},
                                                    ),
                                                    html.Strong(
                                                        ["Promotin 2"],
                                                        style={
                                                            "color": "#515151"},
                                                    ),
                                                    html.P(
                                                        [
                                                            "not yet."
                                                        ],
                                                        style={
                                                            "color": "#7a7a7a"},
                                                    ),
                                                ],
                                                className="nine columns",
                                            ),
                                        ],
                                        className="row",
                                        style={
                                            "background-color": "#f9f9f9",
                                            "padding-bottom": "30px",
                                        },
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
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

# Correlation Matrix with plotly:

##################
# page 4: Correlations 
##################
# Correlation Matrix with plotly:
@app.callback(
    Output('corr_matrix', 'figure'),
    [Input('corr_selector', 'value')]
)
def corr_graph(corr_selector):
    # limit columns since RAM Heroku limited
    df_corr = df[['Store','DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo',    'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance','PromoInterval']]
    value_x = ['Store','DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo',    'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance','PromoInterval']
    data = [
        go.Heatmap(
            z=df_corr.corr(),
            # x=['Store', 'DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance', 'PromoInterval'],
            # y=['Store', 'DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance', 'PromoInterval'],
            ids= value_x,
            colorscale='Viridis',
            reversescale=False,
            type= 'heatmap',
            opacity=0.8,
        )
    ]
    layout = go.Layout(
        xaxis=dict(ticks='', nticks=36),
        yaxis=dict(ticks=''),
        width=600, height=600)
    fig2 = go.Figure(data=data, layout=layout)
    return fig2