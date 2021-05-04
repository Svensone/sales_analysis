import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pathlib

from utils import Header, make_dash_table, make_dash_table_w_header
from variables import color_a, color_b, color_c, color_d, color_extralight, color_bg, color_light, color_main_light, color_main, color_dark_light, color_dark, color_transparent, color_contr, color_contr2

import pandas as pd
pd.options.mode.chained_assignment = None

##############################################################
#  to-dos:
# add average monthly sales and subplot with pct change
# add factorplot with day of week sales
# horziontal table and Chart for second row
# - https://plotly.com/python/figure-factory-subplots/
##############################################################

def create_layout(app, df):
    # Data Table Overview
    ######################
    list1 = ['Sales', 'Customers', "SalesPerCustomer"]
    list2 = ['.max()', '.min()', '.mean()', '.std()']
    rows = []
    for type in list1:
        Series = df[type]
        row = [type, Series.max(), Series.min(), Series.mean().round(2), Series.std().round(2)]
        rows.append(row)
    df_table1 = pd.DataFrame(rows, columns=[' ','Max', 'Min', 'Mean', 'Std. Deviation'])
    df_table1 = df_table1.round(1)

    # Bar Graph Yearly Sales/Customer Overview
    ######################
    year_sales = df.groupby(['Year'])['Sales'].sum().to_frame()
    year_customers = df.groupby(['Year'])['Customers'].sum().to_frame()
    df_barGraph = pd.merge(year_sales, year_customers, how='left', on='Year')
    
    # # Pie Graph - Sales-Storetype Percentage
    sales_storetype = df.groupby(['StoreType'])['Sales'].sum().to_frame()
    sales_storetype.columns = ['total_sales']
    data_pie_storetype = [
        dict(
            type='pie',
            labels= sales_storetype.index,
            values= sales_storetype['total_sales'],
            name='Storetype Sales',
            marker=dict(
                colors=[color_a, color_b, color_c, color_d],
            ),
        )]
    fig_sales_storetype = go.Figure(data= data_pie_storetype)
    fig_sales_storetype.update_layout(showlegend=False)

    return html.Div(
        [
            html.Div([Header(app)]),
            html.Div(
                [
                    # Abstract Row
                    ##############
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Sales Analysis Summary"),
                                    html.Br([]),
                                    html.P(["Rossmann is a large multi-national drugstore chain from Germany with over 3.000 stores all over Europe",
                                            'Sales data from 1.115 german Rossmann-stores from Jan. 2013 until Juli 2015. Additional googletrends and weather data for this time.',
                                            html.Br(),
                                            ], style={"color": "#ffffff"},),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Key Findings Row
                    ##############
                    html.Div(
                        [
                            html.Div(
                                [
                                    
                                    html.H6(
                                        ["Key-Findings "],
                                        className="subtitle padded"),
                                    html.Br(),
                                    html.P([
                                        '   * strong seasonality within a fiscal year with peak before christmas', html.Br(),
                                        '   * heighest sales on monday within a week', html.Br(),
                                        '   * stationarity proven with Dickey-Fuller Test', html.Br(),
                                        '   * pos. correlation between customers and sales as well as running a promotion (only Promotion1 not Promotion2)', html.Br(),
                                    ],
                                    style={
                                        "background-color": "#f9f9f9",
                                        },
                                    ),
                                    html.Br(),
                                ],
                            )
                        ],
                        className="row ",
                    ),
                    ##################
                    # Row Table and Bar Graph year
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Daily Metrics per Store"], className="subtitle padded"),
                                    html.Table(make_dash_table_w_header(df_table1), 
                                    className='table'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Total Annual Sales & Customer",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=df_barGraph.index,
                                                    y=df_barGraph.Sales,
                                                    marker={"color": color_bg,
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 1,
                                                        },
                                                    },
                                                    name="Sales in B",
                                                ),
                                                go.Bar(
                                                    x=df_barGraph.index,
                                                    y=df_barGraph.Customers,
                                                    marker={
                                                        "color": color_dark,
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 1,
                                                        },
                                                    },
                                                    name="Customers in M",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                bargap=0.35,
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    ##################      
                    # Overview Sales / Customer / SalesPerCustomer
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Rossmann Monthly KPIs", className="subtitle padded"),
                                    html.Div([
                                        dcc.Graph(
                                            id='overview_graph',
                                            # config={"displayModeBar": False},
                                        ),
                                        dcc.Dropdown(
                                            id='overview_selectors',
                                            options=[
                                                {"label": "Total", "value": 'total'},
                                                {"label": "Storetype 'A", "value": 'a'},
                                                {"label": "Storetype 'B", "value": 'b'},
                                                {"label": "Storetype 'C", "value": 'c'},
                                                {"label": "Storetype 'D", "value": 'd'},
                                            ],
                                            value='total',
                                            clearable=False,
                                        ),
                                        html.Br(),
                                        html.Br(),
                                    ])
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    ##################      
                    # Total Sales percentage
                    ##################
                    html.Div(
                        [
                            # Pie Sales total per stortype
                            html.Div(
                                [
                                    html.H6("Storetype % of Sales",
                                            className="subtitle padded"),
                                    dcc.Graph(
                                        id='pie_store',
                                        figure=fig_sales_storetype,
                                        # config={"displayModeBar": False},
                                    ),
                                ],
                                className="five columns",
                            ),
                            # Assortment Type Sales-%
                            html.Div(
                                [
                                    html.H6(
                                        "Assortment Type Sales pct of Total",
                                        className="subtitle padded",
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        # style={"margin-bottom": "35px"},
                    ),

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
