import dash_html_components as html
import dash_core_components as dcc
import pandas as pd

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("dash-financial-logo.png"),
                        className="logo",
                    ),
                    html.A(
                        html.Button("About Me", id="learn-more-button"),
                        href="https://portfolio-sven.netlify.app/",
                        target='_blank',
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Financial Analysis and Prediction Rossmann Sales")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header

def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview1",
                className="tab first",
            ),
            dcc.Link(
                "Explorative Analysis",
                href="/dash-financial-report/explAnalysis",
                className="tab",
            ),
            # dcc.Link(                         # in the making
            #     "Time-Series",
            #     href="/dash-financial-report/time_series",
            #     className="tab",
            # ),
            dcc.Link(
                "Correlations", 
                href="/dash-financial-report/correlations", 
                className="tab"
            ),
            dcc.Link(
                "AI Sales Predictions",
                href="/dash-financial-report/predictions",
                className="tab",
            ),
            # dcc.Link(                         # in the making
            #     "Reviews",
            #     href="/dash-financial-report/review",
            #     className="tab",
            # ),
        ],
        className="row all-tabs",
    )
    return menu

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]], ))
        table.append(html.Tr(html_row))
    return table

def make_dash_table_list(list):
    """ Return a dash definition of an HTML table for a list """
    table = []
    for index, row in enumerate(list):
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]], ))
        table.append(html.Tr(html_row))
    return table
    
def make_dash_table_w_header(df):
    table = []
    column_names = df.columns
    html_header = []
    for column in column_names:
        html_header.append(html.Td(column))
    table.append(html.Tr(html_header))
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table