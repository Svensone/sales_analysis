import dash_html_components as html
from utils import Header
import pandas as pd

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # Disclaimer row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Disclamer "],
                                        className="disclaimer padded"),
                                    # html.P('coming soon see'),
                                    html.Strong(
                                        "COMING SOON    --- Full Financial Analysis with interactive graphs at:"),
                                    html.Br(),
                                    html.A(
                                        html.Button(
                                            "Github", className="disclaimer_button"),
                                        href="https://github.com/Svensone/kaggle/blob/main/Competitions/Sales_Performance_Analysis_%26_Prediction_Rossmann.ipynb",
                                        target='_blank',
                                    ),
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
