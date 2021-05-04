import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from utils import Header
from data import complete_data
import pathlib

# data path
PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data")  # .resolve
# df1 = pd.read_csv(DATA_PATH.joinpath('data_full.csv'), low_memory=False)

def create_layout(app, df):
    # df1 = complete_data()[:5] # long time
    df1 = pd.read_csv(DATA_PATH.joinpath('data_full.csv'), low_memory=False)
    df1 = df1[:5]

    fig_table = go.Figure(
        data=[
            go.Table(
            header=dict(
                values=list(df1.columns[:3]),
                # fill_color='blue',
                align='left',
            ),
            cells= dict(
                values=[df1.Sales, df1.Customers, 
                df1.SalesPerCustomer],
                align='left',
            )
        )]
    )

    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1
                    ###########
                    html.Div(
                        [
                            # Findings
                            html.Div(
                                [
                                    html.H6("Test", className="subtitle padded"),
                                    html.Div(
                                        [
                                            html.P(
                                                "Datatable test"
                                            ),
                                            dcc.Graph(figure=fig_table)
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                            ),
                        ],
                        className="row ",
                    ),
                    # Row 
                    ###########
                    html.Div(
                        [
                            # Findings
                            html.Div(
                                [
                                    html.H6("Findings", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "Dummy Text"
                                            ),
                                            html.P(
                                                "Dummy text"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                            # Further Analysis needed
                            html.Div(
                                [
                                    html.H6("Further Analysis", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li("effects of weather on sales"),
                                            html.Li("reason why Promo2 not effective or by coincidence occur with other events"),
                                            html.Li("add socio_economic data, stores in richer regions (Munich, Schwabing) might display different sales than drugstore in rural places"),
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                "dummy text"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    ),
                    # Test Row



                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
