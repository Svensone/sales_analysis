import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_dangerously_set_inner_html

import dash_html_components as html
from utils import Header

import pandas as pd


def create_layout(app, df):
    img_test = app.get_asset_url('bg.jpg')
    html_test = app.get_asset_url('plotly_fb_test.html')
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
                                        [' inner html ']),
                                    # html.Div([
                                    #     dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
									# 		'''

									# 		'''),
                                    # ])
                                ],
                            )
                        ],
                        className="row ",
                    ),
                    # Disclaimer row
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6(
                    #                     ["Facebook Prophet - Future Sales Prediction "],
                    #                     className="disclaimer padded"),
                    #                 html.H6([
                    #                     'with dangerously set inner html'
                    #                 ]),
                    #                 # # with callback
                    #                 # dcc.Input(
                    #                 #     id='html_figure_input', value='initial value', type="text"),
                    #                 # html.H4('Use Pandas HTML Export!'),
                    #                 # html.Div(id='html_figure')
                    #                 # with dangerously set
                    #                 html.Div([
                    #                 ])
                    #             ],
                    #         )
                    #     ],
                    #     className="row ",
                    # ),
                    # IFrame Row
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(['.html file in html.Img() not working']),
                                    html.Iframe(src=html_test,
                                        style={
                                            'display': 'block',
                                            'width': '100%',
                                            "height": "100%",
                    						'border': 'none',
                    						'position': 'absolute',
                    						'top': 0,
                    						'left': 0,
                                        }
                    				),
                                ], style={
                                    'position': 'relative',
                    				'padding': '90%',
                                    "width": '100%',
                                    }
                            )
                        ],
                        className="row ",
                    ),
                    # Disclaimer row
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.H6(
                    #                     [' NOT CLEAN - need resize etc. Test with Iframe ']),
                    #                 html.Div([
                    #                     html.Iframe(src=html_test),
                    #                 ], style={'height': '70vh'}),
                    #             ],
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
