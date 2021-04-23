import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table, make_dash_table_w_header

import pandas as pd
pd.options.mode.chained_assignment = None
import pathlib

# COLOR_VAR
color_extralight = 'rgb(247,251,255)'
color_bg = 'rgb(222,235,247)'
color_main = 'rgb(33,113,181)'
color_dark = 'rgb(8,48,107)'

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
    df_table1 = pd.DataFrame(rows, columns=['Name','Max', 'Min', 'Mean', 'Std. Deviation'])

    # Bar Graph Yearly Sales/Customer Overview
    ######################
    year_sales = df.groupby(['Year'])['Sales'].sum().to_frame()
    year_sales['Sales'] = (year_sales.Sales / 10000000).astype(int)
    year_customers = df.groupby(['Year'])['Customers'].sum().to_frame()
    year_customers['Customers'] = (year_customers.Customers / 1000000).astype(int)
    df_barGraph = pd.merge(year_sales, year_customers, how='left', on='Year')

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
                                            'Sales data from 1.115 german Rossmann stores from Jan. 2013 until Juli 2015. Additional googletrends and weather data for this time.',
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
                                        className="disclaimer padded"),
                                    html.P([
                                        '   * strong seasonality within a fiscal year with peak before christmas', html.Br(),
                                        '   * heighest sales on monday within a week', html.Br(),
                                        '   * stationarity proven with Dickey-Fuller Test', html.Br(),
                                        '   * pos. correlation between nr. of customers and sales as well as running a promotion', html.Br(),
                                    ],
                                    style={
                                        "background-color": "#f9f9f9",
                                        },
                                    ),
                                    html.Br([]),
                                ],
                            )
                        ],
                        className="row ",
                    ),
                    ##################      
                    # Overview Sales / Customer / SalesPerCustomer
                    ##################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Rossmann Overview", className="subtitle padded"),
                                    html.Div([
                                        dcc.Dropdown(
                                            id='overview_selectors',
                                            options=[
                                                {"label": "Storetype 'A", "value": 'a'},
                                                {"label": "Storetype 'B", "value": 'b'},
                                                {"label": "Storetype 'C", "value": 'c'},
                                                {"label": "Storetype 'D", "value": 'd'},
                                            ],
                                            value='a',
                                            clearable=False,
                                        ),
                                        dcc.Graph(
                                            id='overview_graph',
                                            # config={"displayModeBar": False},
                                        ),
                                    ])
                                ],
                                className="twelve columns",
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
                                    html.H6(["Overview"], className="subtitle padded"),
                                    html.Table(make_dash_table_w_header(df_table1), className='table'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Total Annual Sales and Customer",
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
                                                autosize=False,
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
                                className="five columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
