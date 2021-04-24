import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
# helper function from utils.py file
from utils import Header, make_dash_table, make_dash_table_list
# statistics
from statsmodels.distributions.empirical_distribution import ECDF
# General
import pandas as pd
import numpy as np
import pathlib

# COLOR_VAR
color_extralight = 'rgb(247,251,255)'
color_bg = 'rgb(222,235,247)'
color_main = 'rgb(33,113,181)'
color_dark = 'rgb(8,48,107)'
color_contr = '#fde725'
color_contr2 = '#b5de2b'

###########################################
# TO DO !!!!!
# Distplot : https://plotly.com/python/distplot/
# Mixed Subplot : https://plotly.com/python/mixed-subplots/
#######################################################

def create_layout(app, df):
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("data")  # .resolve()
    df_sales_raw = pd.read_csv(DATA_PATH.joinpath(
        'train.csv'), low_memory=False, parse_dates=True, index_col="Date")
    df_stores_raw = pd.read_csv(DATA_PATH.joinpath(
        'store.csv'), low_memory=False, parse_dates=True)

    # Row 1 - CDF and General Data on Datasets
    #####################
    # since slow App - reduce calculation load - see data.py for calculation
    total_count = 1017209
    no_salesClosed_count = 172871
    unique_storetypes = 4
    unique_assortmentTypes = 3
    count_stores_assortment = {'a': 444875, 'b': 8209 , 'c': 391254}
    count_stores_storetype = {'a': 457042, 'b': 15560 , 'c': 112968, 'd': 258768 }
    sales_data_overview = [
        ['Total Number of Sales entries', total_count],
        ['Days with no Sales-value', no_salesClosed_count],
    ]
    store_data_overview = [
        ['Nr of Storetypes', 4], #df.StoreType.unique().shape[0]
        ['Nr. of different Assortment levels', 3], # df.Assortment.unique().shape[0]
    ]

    # ECDF graph
    data_ecdf_sales = np.unique(df_sales_raw["Sales"])
    data_ecdf_cust = np.unique(df_sales_raw['Customers'])
    y_Sales = ((ECDF(df_sales_raw['Sales']))(data_ecdf_sales))
    y_Customers = ((ECDF(df_sales_raw['Customers']))(data_ecdf_cust))

    fig_ecdf = make_subplots(rows=2, cols=1)
    fig_ecdf.append_trace(go.Scatter(
        x = data_ecdf_sales,
        y = y_Sales,
        # y = ((y_Sales)(data_ecdf_sales)),
        line=dict(
                    color=color_dark, 
                    width=3,),
        name= "Empirical Cumulative Distr. of daily Sales",
        mode="lines",
    ), row=1, col=1)
    fig_ecdf.append_trace(go.Scatter(
        x = data_ecdf_cust,
        y = y_Customers,
        line=dict(
                    color=color_bg, 
                    width=3,),
        name= "Empirical Cumulative Distr. of daily Customers",
        mode="lines",
    ), row=2, col=1)
    fig_ecdf.update_layout(
        font=dict(
            family='Helvetica',
        ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        hovermode="closest",
        legend={
            # "x": -0.0228945952895,
            # "y": -0.189563896463,
            "orientation": "h",
            "yanchor": "top",
        },
        xaxis = dict(
            ),
        margin={
            "r": 10,
            "t": 30,
            "b": 30,
            "l": 30,
        },
        showlegend=True,
    )

    # Row 2 : Missing Values Analysis
    #################
    # for faster App loading (see data.py for calculation):
    # Pie Sales Values Missing
    labels_pie = ['Sunday', 'Holiday', 'Others']
    values_pie = [[141137, 0, 31680]]
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

    # Pie Store Values Missing
    data_1 = df_stores_raw.isnull().sum().to_frame()
    data_1 = data_1[(data_1[0] != 0)]
    data_1.columns = ['missing_values']
    data_pie_stores = [
        dict(
            type='pie',
            labels= data_1.index,
            values= data_1['missing_values'],
            title='Store Dataset: Values Missing',
            name='Missing Values',
            marker=dict(
                colors=px.colors.sequential.Viridis,
            ),
        )
    ]
    pie_fig_store = go.Figure(data=data_pie_stores)
    
    # Row 3 - Distplot Sales
    #####################
    # Distplot Sales per Storetype

    # RAM overload if for all
    # hist_a = df[df['StoreType']== 'a']['Sales']
    # hist_b = df[df['StoreType'] == 'b']['Sales']
    # hist_c = df[df['StoreType']== 'c']['Sales']
    # hist_d = df[df['StoreType'] == 'd']['Sales']
    # using 4 random Stores from each StoreType Group as "Representatives" - calculation for all to long
    # stores_a = df[df['StoreType'] == 'a']['Store'].unique()
    # stores_b = df[df['StoreType'] == 'b']['Store'].unique()
    # stores_c = df[df['StoreType'] == 'c']['Store'].unique()
    # stores_d = df[df['StoreType'] == 'd']['Store'].unique()


    # store_a = 1098 #np.random.choice(store_a, 1)
    # store_b = 676 #np.random.choice(store_b, 1)
    # store_c = 869 #np.random.choice(store_c, 1)
    # store_d = 118 #np.random.choice(store_d, 1)
    # hist_a = df[df['Store']== store_a]['Sales']
    # hist_b = df[df['Store'] == store_b]['Sales']
    # hist_c = df[df['Store']== store_c]['Sales']
    # hist_d = df[df['Store'] == store_d]['Sales']

    # hist_data = [hist_a, hist_b, hist_c, hist_d]
    # group_label = ['Storetype A', 'Storetype B', 'Storetype C', 'Storetype D'] 
    
    # fig_distplot = ff.create_distplot(
    #     hist_data, 
    #     group_label, 
    #     colors = [color_contr2, color_dark, color_contr, color_main]
    #     ) # customize bin size = bin_size=[.1, .25, .5, 1]
    # fig_distplot.update_layout(
    #     # title= 'Distplot',
    #     font=dict(
    #         family='Helvetica',
    #     ),
    #     autosize=True,
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     # height=400,
    #     # hovermode="closest",
    #     barmode = 'group',
    #     legend={
    #         # "x": -0.0228945952895,
    #         # "y": -0.189563896463,
    #         "orientation": "h",
    #         "yanchor": "top",
    #     },
    #     margin={
    #         "r": 10,
    #         "t": 30,
    #         "b": 30,
    #         "l": 30,
    #     },
    #     showlegend=True,
    # )
    # fig_sales_distplot = fig_distplot
    # # with plotly Express
    # # fig_sales_distplot=  px.histogram(df['Sales'], x="Sales", marginal="rug")

    # # Pie Graph 2 - Sales-Storetype Percentage
    # sales_storetype = df.groupby(['StoreType'])['Sales'].sum()
    # data_pie_stores = [
    #     dict(
    #         type='pie',
    #         labels=list(sales_storetype.index),
    #         values=list(sales_storetype),
    #         name='Storetype',
    #         title="Storetypes: Pct. of Sales",
    #         insidetextorientation='radial',
    #         marker=dict(
    #             colors=px.colors.sequential.Viridis,
    #         ),
    #     ),
    # ]
    # sales_fig_store = go.Figure(data=data_pie_stores,)

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
                                        figure=fig_ecdf,
                                    )
                                ],
                                className="eight columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row Distribution - Change to Displot with Storetypes/Assortment/
                    ##################
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6("Test",
                    #                         className="subtitle padded"),
                    #                 dcc.Graph(
                    #                     id="graph_histo",
                    #                     figure= fig_sales_distplot,
                    #                 )
                    #             ],
                    #             className="twelve columns",
                    #         ),
                    #     ],
                    #     className="row ",
                    # ),

                    
                    # Row Distribution
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Test2",
                                            className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph_histo_kde_rug",
                                    ),
                                ],
                                className="eight columns",
                            ),
                            # Pie Sales total per stortype
                            html.Div(
                                [
                                    html.H6("Sales of Storetypes",
                                            className="subtitle padded"),
                                    # dcc.Graph(
                                    #     id='pie_store',
                                    #     figure=sales_fig_store,
                                    #     config={"displayModeBar": False},
                                    # ),
                                ],
                                className="four columns",
                            ),
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
                                        figure= pie_fig_store,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            )
                        ],
                        className="row ",
                    ),
                    ##################
                    # Row Outlier test with plotly
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
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
