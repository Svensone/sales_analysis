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
from variables import color_a, color_b, color_c, color_d, color_extralight, color_bg, color_light, color_main_light, color_main, color_dark_light, color_dark, color_transparent, color_contr, color_contr2

###########################################
# TO DO !!!!!
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
        ['Average Sales per Store (month)', 'n'],
        ['Average daily Sales per Customer ', 'not yet'],
    ]
    store_data_overview = [
        ['Nr of Storetypes', 4], #df.StoreType.unique().shape[0]
        ['Nr. of different Assortment levels', 3], # df.Assortment.unique().shape[0]
        ['Mean Distance to Competitor', '5404m'], #df.CompetitionDistance.mean()
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
    ), 
    row=1, col=1)
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

    # Row 2 - Distplot Sales
    #####################
    # Distplot Sales per Storetype
    # RAM overload if for all storetype with e.g hist_a = df[df['StoreType']== 'a']['Sales']
    # using 4 random Stores from each StoreType Group as "Representatives" - shorten calculation time
    store_a = 1098; store_b = 676; store_c = 869; store_d = 118 #using np.random.choice(store_d, 1) see data.py for
    hist_a = df[df['Store']== store_a]['Sales']
    hist_b = df[df['Store'] == store_b]['Sales']
    hist_c = df[df['Store']== store_c]['Sales']
    hist_d = df[df['Store'] == store_d]['Sales']
    hist_data = [hist_a, hist_b, hist_c, hist_d]
    group_label = ['Storetype A', 'Storetype B', 'Storetype C', 'Storetype D'] 
    # with plotly Express: fig_distplot=  px.histogram(df['Sales'], x="Sales", marginal="rug")
    fig_distplot = ff.create_distplot(
        hist_data, 
        group_label, 
        bin_size= 100, # customize bin size = bin_size=[.1, .25, .5, 1]
        colors = [color_a, color_b, color_c, color_d]
        ) 
    fig_distplot.update_layout(
        # title= 'Distplot',
        # font=dict(
        #     family='Helvetica',
        # ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # height=400,
        # hovermode="closest",
        barmode = 'group',
        legend={
            # "x": -0.0228945952895,
            # "y": -0.189563896463,
            "orientation": "h",
            "yanchor": "top",
        },
        margin={
            "r": 10,
            "t": 30,
            "b": 30,
            "l": 30,
        },
        showlegend=True,
    )

    # Row Customer Distribution
    ##################
    fig_distplot2 = px.histogram(df, x="Customers", color="StoreType",
                marginal="violin", # or violin, rug
                hover_data=['Customers', 'Sales'], # df.columns
                nbins=500,
                color_discrete_sequence = [color_a, color_b, color_c, color_d],
    )
    fig_distplot2.update_layout(
        # title= 'Distplot',
        # font=dict(
        #     family='Helvetica',
        # ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        # height=300,
        # hovermode="closest",
        barmode = 'group',
        legend={
            # "x": -0.0228945952895,
            # "y": -0.189563896463,
            "orientation": "h",
            "yanchor": "top",
        },
        # margin={
        #     "r": 10,
        #     "t": 30,
        #     "b": 30,
        #     "l": 30,
        # },
        showlegend=True,
        xaxis = dict(
            title_text = ' ',
            # title_standoff = 25
            ),
        yaxis = dict(
        # title_standoff = 5,
        ),
    )

    # Row: Missing Values Analysis
    #################
    # for faster App loading (see data.py for calculation):
    # Pie Sales Values Missing
    labels_pie = ['Sunday', 'Holiday', 'Others']
    values_pie = [141137, 0, 31680]
    data_pie = [
        dict(
            type='pie',
            labels=labels_pie,
            values=values_pie,
            name='Missing Values in Dataset',
            marker=dict(
                colors=[color_bg, color_main, color_dark]
            ),
        ),]
    pie_fig = go.Figure(data=data_pie)
    pie_fig.update_layout(legend=dict(
        x=0,
        y=1,
        traceorder="reversed",
        # title_font_family="Times New Roman",
        font=dict(
            # family="Courier",
            size=12,
            color="black"
        ),
        bgcolor= 'rgba(0,0,0,0)',
        bordercolor= color_dark,
        borderwidth=2,
        ),
        showlegend=False,
        title= 'Sales',
    )
    # Pie Store Values Missing
    data_1 = df_stores_raw.isnull().sum().to_frame()
    data_1 = data_1[(data_1[0] != 0)]
    data_1.columns = ['missing_values']
    data_pie_stores = [
        dict(
            type='pie',
            labels= data_1.index,
            values= data_1['missing_values'],
            name='Missing Values',
            marker=dict(
                colors=[color_bg, color_main, color_dark, color_light, color_dark_light ],
            ),
        )
    ]
    pie_fig_store = go.Figure(data=data_pie_stores)
    pie_fig_store.update_layout(
        showlegend=False, 
        title='Store Dataset',
        )
    
    return html.Div(
        [
            Header(app),
            html.Div(
                [
                    # Row General Data
                    ############
                    html.Div(
                        [
                            html.H5(['Statistical and explorative Analysis'],
                                            className="subtitle padded",
                                            style={
                                                # 'paddingBottom': "30",
                                                # 'paddingTop': '30',
                                                }
                                            ),
                            html.Br([]),
                            html.Div(
                                [
                                    html.H6(
                                        ["Sales Data"], 
                                        className="subtitle padded"
                                    ),
                                    html.Br([]),
                                    html.Table(make_dash_table_list(
                                        sales_data_overview), className='table'),
                                    html.H6(
                                        ["Stores Data"], className="subtitle padded"
                                    ),
                                    html.Br([]),
                                    html.Br([]),
                                    html.Table(make_dash_table_list(
                                        store_data_overview), className='table'),
                                ],
                                className="five columns",
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
                                className="seven columns",
                                style={'paddingLeft': "100"}
                            ),
                        ],
                        className="row ",
                    ),
                    # Row Distplot
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Distribution of Sales Values ",
                                            className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph_histo",
                                        figure= fig_distplot,
                                    )
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Row Customer Distribution
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Customer Distribution",
                                            className="subtitle padded"),
                                    # dcc.RadioItems(
                                    #     id='customer_dist_selector',
                                    #     options=[
                                    #         {'label': x, 'value': x} for x in ['total', 'Storetype']
                                    #         ],
                                    #     value='total'),
                                    dcc.Graph(
                                        id="customer_dist",
                                        figure=fig_distplot2,
                                    ),
                                ],
                                className="twelve columns",
                            ),
                            # # Pie Sales total per stortype
                            # html.Div(
                            #     [
                            #         html.H6("Storetype % of Sales",
                            #                 className="subtitle padded"),
                            #         dcc.Graph(
                            #             id='pie_store',
                            #             figure=fig_sales_storetype,
                            #             # config={"displayModeBar": False},
                            #         ),
                            #     ],
                            #     className="five columns",
                            # ),
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
                    # Row Outlier test with plotly = move to profitability page
                    # https://plotly.com/python/v3/outlier-test/
                    ##################
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6("Outlier Detection",
                    #                         className="subtitle padded"),
                    #                 html.Img(
                    #                     src=app.get_asset_url(
                    #                         'img/outlier_detection_sns.jpg'),
                    #                     style={'width': '100%'}
                    #                 ),
                    #             ],
                    #             className="twelve columns",
                    #         )
                    #     ],
                    #     className="row ",
                    # ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
