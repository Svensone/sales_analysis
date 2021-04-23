# Disclaimer row building block
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

def get_disclaimer_block():
    block = html.Div([
        html.Div(
            [
                html.H6(["Disclamer "], className="disclaimer padded"), html.P(
                    'interactive Graph coming soon see Financial Analysis with interactive graphs at:'),
                html.A(
                    html.Button("Github", className="disclaimer_button"),
                    href="https://github.com/Svensone/kaggle/blob/main/Competitions/Sales_Performance_Analysis_%26_Prediction_Rossmann.ipynb",
                    target='_blank'),
            ],
        )
    ],
        className="row ",
    ),
    return block

# Image Block

def get_image_block(img_path):
    return html.Div([html.Div(
        [
            html.H6(["Time Series "], className="disclaimer padded"),
            html.Strong(""),
            html.Br(),
            html.Img(src=img_path,
                    style={'width': '100%'})
        ],
    )
    ],
        className="row ",
    ),
