import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# helper function from utils.py file
from utils import Header, make_dash_table, make_dash_table_list

# statistics
from statsmodels.distributions.empirical_distribution import ECDF

import pandas as pd
import numpy as np
import pathlib

# COLOR_VAR
color_extralight = 'rgb(247,251,255)'
color_bg = 'rgb(222,235,247)'
color_main = 'rgb(33,113,181)'
color_dark = 'rgb(8,48,107)'

###########################################
# TO DO !!!!!

# Distplot : https://plotly.com/python/distplot/
# Mixed Subplot : https://plotly.com/python/mixed-subplots/
#######################################################

def create_layout(app):
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("data")  # .resolve()
    # 1. Full set
    df_total = pd.read_csv(DATA_PATH.joinpath('clean.csv'), low_memory=False, parse_dates=True)
    # 
    df_sales_raw = pd.read_csv(DATA_PATH.joinpath('train.csv'), low_memory=False, parse_dates=True, index_col="Date")
    df_stores_raw = pd.read_csv(DATA_PATH.joinpath('store.csv'), low_memory=False, parse_dates=True)

    # Table 1
    sales_data_overview =[
        ['Total Number of Sales entries', df_sales_raw.shape[0]],
        ['Days with no Sales-value', df_sales_raw[(df_sales_raw.Sales == 0)].shape[0]],
    ]
    store_data_overview = [
        ['Nr of Storetypes', df_total.StoreType.unique().shape[0]],
        ['Nr. of different Assortment levels', df_total.Assortment.unique().shape[0]],
        ['Average Monthly Sales per Storetype', " "],
    ]

    # ECDF graph
    ################################
    data_ecdf = df_sales_raw["Sales"]
    ecdf_sales = ECDF(data_ecdf)
    fig_ecdf = go.Figure()
    fig_ecdf.add_scatter(
        x=np.unique(data_ecdf), 
        y=( ecdf_sales)(np.unique(data_ecdf))
        )

    # PIE GRAPH Sales
    #################
    sunday = df_sales_raw[(df_sales_raw.DayOfWeek == 7) & (df_sales_raw.Sales == 0)].shape[0]
    holiday = df_sales_raw[(df_sales_raw.StateHoliday == 0) & (df_sales_raw.Sales == 0)].shape[0]
    total = sales_missing_values = df_sales_raw[(df_sales_raw.Open == 0) & (df_sales_raw.Sales == 0)].shape[0]
    others = total - sunday - holiday
    labels_pie = ['Sunday', 'Holiday', 'Others']
    values_pie = [sunday, holiday, others]

    data_pie = [
        dict(
            type='pie',
            labels=labels_pie,
            values=values_pie,
            title='Sales Values Missing',
            name='Missing Values in Dataset',
            marker=dict(
                colors=[color_bg, color_main, color_dark]
            ),
        ),
    ]
    pie_fig = go.Figure(data=data_pie)


    # Pie Graph: Missing Values Stores-Dataset
    data_1 = df_stores_raw.isnull().sum().to_frame()
    labels_1 = data_1.index
    values_1 = data_1[0]

    data_pie_stores = [
        dict(
            type='pie',
            labels=labels_1,
            values= values_1,
            title='Store Dataset: Values Missing',
            name='Missing Values',
            marker=dict(
                colors= px.colors.sequential.Viridis,
            ),
        )
    ]
    pie_fig_store = go.Figure(data=data_pie_stores)

    # Pie Graph 2 - Sales-Storetype Percentage
    ###########################
    nr_storetypes = df_total.groupby(['StoreType'])['Sales'].sum()
    labels_storetype = list(nr_storetypes.index)
    sales_storetype = list(nr_storetypes)
    data_pie_stores = [
        dict(
            type='pie',
            labels=labels_storetype,
            values=sales_storetype,
            name='Storetype',
            title="Storetypes: Pct. of Sales",
            insidetextorientation='radial',
            marker=dict(
                colors=px.colors.sequential.Blues,
            ),
        ),
    ]
    sales_fig_store = go.Figure(data=data_pie_stores,)

    return html.Div(
        [
            Header(app),
            html.Div(
                [
                    # Row General Data
                    ############
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Sales Data"], className="subtitle padded"
                                    ),
                                    html.Br([]),
                                    html.Table(make_dash_table_list(
                                        sales_data_overview), className='table'),
                                    html.H6(
                                        ["Stores Data"], className="subtitle padded"
                                    ),
                                    html.Br([]),
                                    html.Table(make_dash_table_list(
                                        store_data_overview), className='table'),
                                ],
                                className="four columns",
                            ),
                            html.Div(
                                [
                                    html.H6("Empirical CDF of Sales",
                                            className="subtitle padded"),
                                    dcc.Graph(
                                        id="ecdf-graph",
                                        figure=fig_ecdf
                                    )
                                ],
                                className="eight columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row Distribution
                    ##################
                    html.Div(
                        [
                        ],
                        className="row ",
                    ),
                    ##################
                    # Row Missing Values
                    ##################
                    html.Div(
                        [
                            html.H6("Missing Values Analysis",
                                    className="subtitle padded"),
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(
                                        id='missing_pie_sales',
                                        figure=pie_fig,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id='missing_pie_store',
                                        figure=pie_fig_store,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 
                    ##################
                    html.Div(
                        [
                            # Bar Graph SpC Storetype
                            # Sunday open - Storetype
                            # Pie Sales total per stortype
                            ################################
                            # remove assortment
                            html.Div(
                                [
                                    html.H6("Sales of Storetypes",
                                            className="subtitle padded"),
                                    dcc.Graph(
                                        id='pie_store',
                                        figure=sales_fig_store,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            )
                        ],
                        className="row ",
                    ),
                    ##################
                    # Row
                    ##################
                    # Row
                    # Outlier test with plotly
                    # https://plotly.com/python/v3/outlier-test/
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Outlier Detection",
                                            className="subtitle padded"),
                                    # html.Img(
                                    #     src=app.get_asset_url(
                                    #         'img/outlier_detection_sns.jpg'),
                                    #     style={'width': '100%'}
                                    # ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    ##################
                    # Row
                    ##################
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )