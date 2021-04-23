# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pathlib
import pandas as pd
import numpy as np
# INFO: data.py not pushed to github / heroku!!
# from data import get_data, get_corr  # connect_gCloud_sql
from pages import (
    overview,
    explAnalysis,
    # time_series,
    correlations,
    predictions,
    review,
)
# Data
########################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data")  # .resolve()
df = pd.read_csv(DATA_PATH.joinpath('clean.csv'), low_memory=False, parse_dates=True)
# df_corr = pd.read_csv(DATA_PATH.joinpath('corr_matrix.csv'), low_memory=False, parse_dates=True)
# From GoogleCloud SQL (not using since expensive, test successful)
# df_sales = connect_gCloud_sql()

# COLOR_VAR
color_extralight = 'rgb(247,251,255)'
color_bg = 'rgb(222,235,247)'
color_main = 'rgb(33,113,181)'
color_dark = 'rgb(8,48,107)'

# SETUP APP & SERVER
#######################
app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# LAYOUT
#######################
app.layout = html.Div(
    [dcc.Location(id="url", refresh=True),
    html.Div(id="page-content")]
)

# on Update switch pages
# #######################
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/explAnalysis":
        return explAnalysis.create_layout(app)
    # elif pathname == "/dash-financial-report/time_series":    # add later when Design clean
    #     return time_series.create_layout(app)
    elif pathname == "/dash-financial-report/correlations":
        return correlations.create_layout(app)
    elif pathname == "/dash-financial-report/predictions":
        return predictions.create_layout(app)
    # elif pathname == "/dash-financial-report/review":         # add later when Design clean
    #     return review.create_layout(app)
    elif pathname == "/dash-financial-report/full-view":
        return (
            overview.create_layout(app, df),
            explAnalysis.create_layout(app),
            # time_series.create_layout(app),
            correlations.create_layout(app,),
            predictions.create_layout(app),
            # review.create_layout(app),
        )
    else:
        return overview.create_layout(app, df),

# INDIVIDUAL CALLBACKS FOR Graphs
#######################
# page 1 overview-graph
##################
@app.callback(
    Output('overview_graph', 'figure'),
    [Input('overview_selectors', 'value')]
)
def overview_graph_1(select):
    # print('Overview Graph Selector :' + select)
    # add rangeslider
    data_overview = df.groupby(['YearMonth_timestamp']).agg({
        'Sales': np.sum,
        'Customers': np.sum,
        'SalesPerCustomer': np.mean
    })
    data_overview['Sales'] = data_overview['Sales'] / 10
    # add percentage change
    bar_list = ['Customers', 'Sales']
    for col in bar_list:
        data_overview[col + '_pct_change'] = (data_overview[col].pct_change(1, fill_method='ffill')) * 100
    # print(data_overview['Sales_pct_change'])
    
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    # Customers
    color_list = [color_dark, color_bg]
    count = 0
    for value in bar_list:
        fig1.add_trace(
            go.Bar(
                name= value,
                x = data_overview.index,
                y = data_overview[value],
                marker_color = color_list[count],
            ),
            secondary_y=False)
        count =+ 1

    count = 0
    for value_pct in bar_list:
        fig1.add_trace(
            go.Scatter(
                name= value_pct + " per month",
                mode="lines", 
                x=data_overview.index, 
                y=data_overview[value_pct + '_pct_change'],
                # fill='tonexty',
                # fillcolor= color_bg,
                marker = dict(
                    color = color_list[count])
            ),
            secondary_y=True,
            )
        count =+ 1

    fig1.update_layout(
        barmode='group',
        font=dict(
            family='Helvetica',
        ),
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        hovermode="closest",
        legend={
            # "x": -0.0228945952895,
            # "y": -0.189563896463,
            "orientation": "h",
            "yanchor": "top",
        },
        xaxis = dict(
            range = ['2013-01-01','2015-07-31'],
            rangeslider = dict(
                visible = True
            ),
            dtick="M1", 
            tickformat="%b\n%Y",
            ticklabelmode="period",
        ),
        xaxis_tickangle=-45,
        margin={
            "r": 10,
            "t": 30,
            "b": 30,
            "l": 30,
        },
        showlegend=True,
    )
    return fig1
    # Working with 2 Scatter Plot line mode
    ##########################
    # fig1.add_trace(
    #     go.Scatter(
    #     name= "Customers per month",
    #     mode="markers+lines", 
    #     x=data_overview.index, 
    #     y=data_overview["Customers"],
    #     # fill='tonexty',
    #     # fillcolor= color_bg,
    #     marker = dict(
    #     color = color_bg)
    # ),
    # secondary_y=True,
    # )
    # fig1.add_trace(
    #     go.Scatter(
    #     name= "Sales per month",
    #     mode="markers+lines", 
    #     x=data_overview.index, 
    #     y=data_overview["Sales"],
    #     # fill='tonexty',
    #     # fillcolor= color_dark,
    #     marker = dict(
    #     color = color_dark)
    # ),
    # secondary_y=False,
    # )   
    # fig1.add_hline(
    #     y= 1950000000,
    #     line_width=3,
    #     line_dash="dash",
    #     line_color='green',
    #     annotation_text="Average Sales",
    #     annotation_position="bottom right",
    # )
    # fig1.update_layout(
    #     font=dict(
    #         family='Helvetica',
    #     ),
    #     autosize=True,
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     height=300,
    #     hovermode="closest",
    #     legend={
    #         # "x": -0.0228945952895,
    #         # "y": -0.189563896463,
    #         "orientation": "h",
    #         "yanchor": "top",
    #     },
    #     xaxis = dict(
    #         range = ['2013-01-01','2015-07-31'],
    #         rangeslider = dict(
    #             visible = True
    #         ),
    #         dtick="M1", 
    #         tickformat="%b\n%Y",
    #         ticklabelmode="period",
    #     ),
    #     margin={
    #         "r": 10,
    #         "t": 30,
    #         "b": 30,
    #         "l": 30,
    #     },
    #     showlegend=True,
    # )

# page 2: explanatory / statistical Data Analysis
##################

# page 3: Time Series - in the making               # in the making
##################
# @app.callback(
#     Output('time-series-graph', 'figure'),
#     [Input('time-series-selector', 'value')])
# def create_timeSeries(selector):
    # df_1 = df.groupby('Date')['SalesPerCustomer'].mean().to_frame()
    # df_1.index = pd.to_datetime(df_1.index)
    # add additional traces
    # values_2 = df.groupby('Date')['SalesPerCustomer'].sum().pct_change()
    # values_2 = df.groupby('Date')['SalesPerCustomer'].sum().rolling(7, center=True)
    # create
    # fig_1 = px.line(df_1, x=df_1.index, y='SalesPerCustomer')
    # fig_1.update_xaxes(rangeslider_visible=True)
    # fig_1.update_layout(paper_bgcolor='rgb(0,0,0,0)',
    #                     hovermode="closest", plot_bgcolor='rgb(0,0,0,0)')
    # return fig_1

##################
# page 4: Correlations 
##################
# Correlation Matrix with plotly:
@app.callback(
    Output('corr_matrix', 'figure'),
    [Input('corr_selector', 'value')]
)
def corr_graph(corr_selector):
    # limit columns since RAM Heroku limited
    df_corr = df[['Store','DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo',    'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance','PromoInterval']]
    value_x = ['Store','DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo',    'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance','PromoInterval']
    data = [
        go.Heatmap(
            z=df_corr.corr(),
            # x=['Store', 'DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance', 'PromoInterval'],
            # y=['Store', 'DayOfWeek', 'Sales', 'Customers', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'Day', 'Year', 'WeekOfYear', 'SalesPerCustomer', 'Promo2', 'StoreType', 'Assortment', 'CompetitionDistance', 'PromoInterval'],
            ids= value_x,
            colorscale='Viridis',
            reversescale=False,
            # type= 'heatmap',
            opacity=0.8,
        )
    ]
    layout = go.Layout(
        xaxis=dict(ticks='', nticks=36),
        yaxis=dict(ticks=''),
        width=600, height=600)
    fig2 = go.Figure(data=data, layout=layout)
    return fig2

#################
# page 5 Review (in the making)
##################

# start app
if __name__ == "__main__":
    app.run_server(debug=True)
