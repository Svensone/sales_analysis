# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#Statistical
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

import json
import pathlib
import pandas as pd
import numpy as np

# INFO: data.py not pushed to github / heroku!!
# from data import get_data, get_corr  # connect_gCloud_sql
from pages import (
    overview,
    explAnalysis,
    test,
    profitability,
    correlations,
    predictions,
    review,
)
from variables import color_a, color_b, color_c, color_d, color_extralight, color_bg, color_light, color_main_light, color_main, color_dark_light, color_dark, color_transparent, color_contr, color_contr2

##############################################################
#  to-dos:
# in App
# https://plotly.com/python/heatmaps/# 
# from Colab import as Html:
# - heatmapz - create in Colab and import as html
# - Outlier Test :  https://plotly.com/python/v3/outlier-test/
# - Implement : js.animation (from Bali homepage) with
# https://community.plotly.com/t/how-can-i-use-my-html-file-in-dash/7740
##############################################################

# Data
########################
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data")  # .resolve()
df = pd.read_csv(DATA_PATH.joinpath('clean.csv'), low_memory=False, parse_dates=True)
# df_full = pd.read_csv(DATA_PATH.joinpath('data_full.csv'), low_memory=False, parse_dates=True)

# From GoogleCloud SQL (not using since expensive, test successful)
# df_sales = connect_gCloud_sql()

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
    [dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")]
)

# on Update switch pages
# #######################
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/explAnalysis":
        return explAnalysis.create_layout(app, df)
    elif pathname == "/dash-financial-report/profitability":    # add later when Design clean
        return profitability.create_layout(app, df)
    elif pathname == "/dash-financial-report/test":
        return test.create_layout(app, df)
    elif pathname == "/dash-financial-report/correlations":
        return correlations.create_layout(app, df)
    elif pathname == "/dash-financial-report/predictions":
        return predictions.create_layout(app, df)
    elif pathname == "/dash-financial-report/review":         # add later when Design clean
        return review.create_layout(app, df)
    elif pathname == "/dash-financial-report/full-view":
        return (
            overview.create_layout(app, df),
            explAnalysis.create_layout(app, df),
            profitability.create_layout(app, df),
            test.create_layout(app, df),
            correlations.create_layout(app, df),
            predictions.create_layout(app, df),
            review.create_layout(app, df),
        )
    else:
        return overview.create_layout(app, df),

# INDIVIDUAL CALLBACKS FOR GRAPHS
#######################
# page 1 overview-graph
#######################
@app.callback(
    Output('overview_graph', 'figure'),
    [Input('overview_selectors', 'value')]
)
def overview_graph_1(select):
    # print('Overview Graph Selector :' + select)
    if select == 'total':
        data_overview = df.groupby(['YearMonth_timestamp']).agg({
            'Sales': np.sum,
            'Customers': np.sum,
        })
    else:
        df1= df[(df.StoreType == select)]
        data_overview = df1.groupby(['YearMonth_timestamp']).agg({
            "Sales": np.sum,
            "Customers": np.sum,
        })
    # print(data_overview.head())
    
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    bar_list = ['Customers', 'Sales']
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
    # add subplot w. shared x-axes for pct-change
    #####################
    # for col in bar_list:
    # data_overview[col + '_pct_change'] = (data_overview[col].pct_change(1, fill_method='ffill')) * 100
   
    # color2 = [ color_contr, color_contr2]
    # count = 0
    # for value_pct in bar_list:
    #     fig1.add_trace(
    #         go.Scatter(
    #             name= value_pct + " % Change",
    #             mode="lines", 
    #             x=data_overview.index, 
    #             y=data_overview[value_pct + '_pct_change'],
    #             # marker = dict(
    #             #     color = color2[count])
    #             line=dict(
    #                 color=color2[count], 
    #                 width=3,
    #                 # dash='dash'
    #                 )
    #         ),
    #         secondary_y=True,
    #         )
    #     count =+ 1
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

# page 2: explanatory / statistical Data Analysis
##################
# Customer Distribution w. Violin
@app.callback(
    Output('customer_dist', 'figure'),
    [Input('customer_dist_selector', 'value')]
)
def cust_dist(select):
    if select == 'total':
        # store_a = 1098; store_b = 676; store_c = 869; store_d = 118 #using np.random.choice(store_d, 1) see data.py for
        hist_a = df['Customers']
        # hist_b = df[df['Store'] == store_b]['Sales']
        # hist_c = df[df['Store']== store_c]['Customers']
        # hist_d = df[df['Store'] == store_d]['Customers']
        hist_data = [hist_a]
        group_label = ['Total Customers'] 
    else:
        # using single stores as "representative" for group to minimize app loading time
        store_a = 1098; store_b = 676; store_c = 869; store_d = 118 #using np.random.choice(store_d, 1) see data.py for
        hist_a = df[df['Store']== store_a]['Customers']
        hist_b = df[df['Store'] == store_b]['Customers']
        hist_c = df[df['Store']== store_c]['Customers']
        hist_d = df[df['Store'] == store_d]['Customers']
        hist_data = [hist_a, hist_b, hist_c, hist_d]
        group_label = ['Storetype A', 'Storetype B', 'Storetype C', 'Storetype D'] 

    # with plotly Express: 
    # fig_cust_plot=  px.histogram(df['Sales'], x="Sales", marginal="rug")
    fig_distplot_cust = ff.create_distplot(
        hist_data, 
        group_label, 
        bin_size= 200, # customize bin size = bin_size=[.1, .25, .5, 1]
        colors = ['#35b779', color_dark, color_contr, color_main]
        ) 
    fig_distplot_cust.update_layout(
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

# page: Seasonality - Trend - Stationarity
##################
# Weekly Seasonality
#############################3
@app.callback(
    Output('seasonality_graph', 'figure'),
    [Input('seasonality_selector', 'value')]
)
def seasonality(store_type_select):

    sales_seasonality = df.groupby(['Date', 'StoreType']).sum()
    sales_seasonality = sales_seasonality.Sales.reset_index().set_index('Date')
    sales_seasonality.index = pd.to_datetime(sales_seasonality.index)
    sales_seasonality = sales_seasonality[sales_seasonality.StoreType == store_type_select]
    sales_seasonality = sales_seasonality['Sales'].astype('float')
    # print(sales_seasonality.head())
    # sales_mean = [2000]
    resample = sales_seasonality.resample('W').sum()
    if store_type_select == 'a':
        color = color_a
    elif store_type_select == 'b':
        color = color_b
    elif store_type_select == 'c':
        color = color_c
    elif store_type_select == 'd':
        color = color_d
    print(color)
    fig = make_subplots(
        rows=3, 
        cols=2,
        specs=[
            [{"colspan":2}, None],
            [{"colspan":2}, None],
            [{"type": "scatter"}, {"type": "table"}],
            ],
        print_grid=True,
        )
    #seasonality line-plot
    fig.add_trace(
        go.Scatter(
            y=resample,
            name='sin',
            # mode='markers',
            marker_color= color,
        ), row=1, col=1)
    # add mean sales horizontal line
    # fig.add_hline(y= 20000000, line_width=3, dash= 'dash', line_color= color_dark)
    # seasonality - monthly
    # decomposition = seasonal_decompose(sales_seasonality, model='additive', period=365)
    # print(decomposition.trend[-20:])
    #test with other values
    timeseries = sales_seasonality
    fig.add_trace(
        go.Scatter(
            # y= timeseries.resample('W').mean()
            ),
            row=2, col=1
            )

    # stationarity - line plot
    timeseries = sales_seasonality
    roll_mean = timeseries.rolling(window=7).mean()
    roll_std = timeseries.rolling(window=7).std()
    fig.add_trace(go.Scatter(y= timeseries.resample('W').mean()), row=3, col=1)
    fig.add_trace(go.Scatter(y= roll_mean.resample('W').mean()), row=3, col=1)
    fig.add_trace(go.Scatter(y= roll_std.resample('W').mean()), row=3, col=1)

    # table dickey-fuller test results
    results_adfuller = adfuller(timeseries, autolag='AIC')
    # print(results_adfuller)
    values_test= [
        ['ADF of Test', 'P-Value', 'Critical Values'], 
        [results_adfuller[0], results_adfuller[1], " "]
        ]
    for key, value in results_adfuller[4].items():
        values_test[0].append(key)
        values_test[1].append(value)
    # print(values_test)
    fig.add_trace(go.Table(
        header=dict(values=['A', 'B']), 
        cells=dict(values= values_test)),
        row=3, col=2,
        )
    fig.update_layout(
        height=700, 
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        )
    return fig

# page: Profitability
##################
@app.callback(
    Output('profi-graph', 'figure'),
    [Input('profi-selector', 'value')])
def create_prof(selector):
    df_1 = df[df.Open != 0]
    subs = df_1[df_1.SalesPerCustomer.notnull()]
    sub = sub[["Sales", 'SalesPerCustomer', 'Store']]

# page Correlations 
##################
# Correlation Matrix with plotly:
@app.callback(
    Output('corr_matrix', 'figure'),
    [Input('corr_selector', 'value')]
)
def corr_graph(corr_selector):
    # limit columns since RAM Heroku limited = using df_full later
    # df_corr1 = df_full[df_full['StoreType'] == corr_selector]
    df_corr1 = df[df['StoreType'] == corr_selector]

    df_corr1 = df_corr1[df_corr1['Open'] != 0]
    df_corr = df_corr1.drop('Unnamed: 0', axis=1)
    # df_corr = df_corr.dropna()
    print(df_corr.columns)
    selected_values = [
        'Sales', 
        'Customers',
        'SalesPerCustomer',
        'DayOfWeek', 
        "Promo",
        "Promo2",
        'Assortment',
        'State',
        'Dayofweek',
        'trend',
        'Mean_TemperatureC',
        'Precipitationmm',
        'CompetitionMonthsOpen',
        ]
    df_corr = df_corr[selected_values]
    # print(df_corr.head())
    df_corr = df_corr.corr()
    # ['Store', 'DayOfWeek', 'Date', 'Sales', 'Customers', 'Open', 'Promo',
    #    'StateHoliday', 'SchoolHoliday', 'Year', 'Month', 'Week', 'Day',
    #    'Dayofweek', 'Dayofyear', 'Is_month_end', 'Is_month_start',
    #    'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start',
    #    'Elapsed', 'SalesPerCustomer', 'StoreType', 'Assortment',
    #    'CompetitionDistance', 'CompetitionOpenSinceMonth',
    #    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek',
    #    'Promo2SinceYear', 'PromoInterval', 'State', 'file', 'week', 'trend',
    #    'Max_TemperatureC', 'Mean_TemperatureC', 'Min_TemperatureC',
    #    'Dew_PointC', 'MeanDew_PointC', 'Min_DewpointC', 'Max_Humidity',
    #    'Mean_Humidity', 'Min_Humidity', 'Max_Sea_Level_PressurehPa',
    #    'Mean_Sea_Level_PressurehPa', 'Min_Sea_Level_PressurehPa',
    #    'Max_VisibilityKm', 'Mean_VisibilityKm', 'Min_VisibilitykM',
    #    'Max_Wind_SpeedKm_h', 'Mean_Wind_SpeedKm_h', 'Max_Gust_SpeedKm_h',
    #    'Precipitationmm', 'CloudCover', 'Events', 'WindDirDegrees',
    #    'StateName', 'CompetitionOpenSince', 'CompetitionDaysOpen',
    #    'CompetitionMonthsOpen', 'Promo2Since', 'Promo2Days', 'Promo2Weeks']
    
    data = [
        go.Heatmap(
            z=df_corr,
            x=df_corr.columns.values,
            y=df_corr.columns.values,
            # ids= value_x,
            colorscale='Blues',
            # reversescale=False,
            type= 'heatmap',
            # opacity=0.8,
            hoverongaps = False,
        )
    ]
    layout = go.Layout(
        xaxis=dict(ticks='', nticks=36),
        yaxis=dict(ticks=''),
        # width=600, height=600,
        )
    fig2 = go.Figure(data=data, layout=layout)
    return fig2

# page: Preditions
##################
# Comparison
@app.callback(
    Output('prediction_graph', 'figure'),
    [Input('prediction_selectors', 'value')]
)
def prediction_graph(select):
    # print(select)
    #daily predictions (31 days) for Store Nr. 12
    # df_proph = pd.read_csv(DATA_PATH.joinpath('prophet', 'fbProphet_pred_31.csv'), parse_dates=True)
    # df_proph.columns = ['id', 'Date', 'Sales']
    # df_fastai = pd.read_csv(DATA_PATH.joinpath('fastai', 'full_prediction_fastAI.csv'), parse_dates=True)
    # df_fastai = df_fastai[df_fastai['Store'] == 12].sort_values('Date')
    # df_fastai = df_fastai[['Date', "Sales"]]
    ## total daily sales forecast 31 days
    df_proph = pd.read_csv(DATA_PATH.joinpath('prophet', 'totalDailySales_fbProphet_pred_31.csv'), parse_dates=True)
    df_proph.columns = ['id', 'Date', 'Sales']
    df_fastai = pd.read_csv(DATA_PATH.joinpath('fastai', 'full_prediction_fastAI.csv'), parse_dates=True)
    df_fastai = df_fastai.groupby('Date').agg({
        'Sales': np.sum
    }).sort_values('Date')
    df_fastai = df_fastai[['Date', "Sales"]]

    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    bar_list = ['Prophet', 'FastAi',] #  'FastAi',  'PowerBI', 'Tableau'
    data_df = [df_proph, df_fastai]
    color_list = [color_dark, color_bg]
    count = 0
    for value in bar_list:
        fig1.add_trace(
            go.Scatter(
                name= value,
                x = data_df[count].Date,
                y = data_df[count].Sales,
                marker_color = color_list[count],
            ),
            secondary_y=False)
        count =+ 1
    fig1.update_layout(
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        hovermode="closest",
        legend={
            "orientation": "h",
            "yanchor": "top",
        },
        xaxis = dict(
            range = ['2015-05-01','2015-08-31'],
            rangeslider = dict(
                visible = True
            ),
            # dtick="M1", 
            # tickformat="%b\n%Y",
            # ticklabelmode="period",
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

# Tableau predictions
# MS PowerBI predictions
# FastAI Neural Net Predictins

# Facebook Prophet
@app.callback(
    Output('prophet_components', 'figure'), 
    [Input('prophet_components_input', "value")]
    )
def prophet_html(btn_clicks):
    cache = 'fig_prophet_components2.json'
    with open (cache, 'r') as f:
        return json.load(f)

# page 5 Review (in the making)
##################


# start app
if __name__ == "__main__":
    app.run_server(debug=True)
