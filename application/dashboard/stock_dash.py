"""Create a Dash app within a Flask app."""
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import plotly.graph_objects as go
from dash import Dash

from .layout import html_layout


def Add_Dash(server):
    """Create a Dash app."""
    external_stylesheets = ['/static/dist/css/styles.css',
                            'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']
    dash_app = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/stockdash/')

    # Override the underlying HTML template
    dash_app.index_string = html_layout

    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div(
        [
            html.H2('Stock Price Analysis after a data breach'),
            html.H3(id="square", style={'color': 'blue', 'fontSize': 22}),
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in
                         ['Facebook', 'Equifax', 'Capital One', 'Under Armour', 'Marriott', 'EBAY']],
                value='Facebook'
            ),
            dcc.Graph(id="graph", style={"width": "100%", "height": "100%", "display": "inline-block"}),
        ]
    )

    # Pass dash_app as a parameter
    init_callbacks(dash_app)

    return dash_app.server


def add_moving_average(df, fig, mavg_50, mavg_200):
    fig.add_trace(
        go.Scatter(
            x=df['Date'], y=mavg_50, name="50 day MA", line_color='red',
            opacity=0.6))

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=mavg_200,
            name="200 day MA",
            line_color='green',
            opacity=0.6))


def init_callbacks(dash_app):
    @dash_app.callback([dash.dependencies.Output('graph', 'figure'), dash.dependencies.Output('square', 'children')],
                       [dash.dependencies.Input('dropdown', 'value')])
    def display_value(value):
        if value == "Facebook":
            start = datetime.datetime(2017, 9, 28)
            end = datetime.datetime(2019, 9, 28)

            df = web.DataReader("FB", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)
            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="FB Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2018-09-28',
                    y0=118,
                    x1='2018-09-28',
                    y1=225,
                    line=dict(color="black", width=2))
            ])
            return fig, html.A("Facebook: 50 million records breached on 28th September, 2018",
                               href="https://www.theguardian.com/technology/2018/sep/28/facebook-50-million-user-accounts-security-berach")
        elif value == "Equifax":
            start = datetime.datetime(2016, 9, 7)
            end = datetime.datetime(2018, 9, 7)

            df = web.DataReader("EFX", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)

            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="EQUIFAX Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2017-09-07',
                    y0=85,
                    x1='2017-09-07',
                    y1=150,
                    line=dict(color="black", width=2))
            ])

            return fig, html.A("Equifax: 143 million records breached on 7th September, 2017",
                               href="https://investor.equifax.com/news-and-events/news/2017/09-07-2017-213000628")
        elif value == "Capital One":
            start = datetime.datetime(2018, 7, 29)
            end = datetime.datetime(2019, 8, 30)

            df = web.DataReader("COF", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)
            df.tail()

            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="Capital One Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2019-07-29',
                    y0=65,
                    x1='2019-07-29',
                    y1=105,
                    line=dict(color="black", width=2))
            ])

            return fig, html.A("Capital One: 106 million records breached on 29th July, 2019",
                               href="http://press.capitalone.com/phoenix.zhtml?c=251626&p=irol-newsArticle&ID=2405043")
        elif value == "Under Armour":
            start = datetime.datetime(2017, 3, 29)
            end = datetime.datetime(2019, 3, 29)

            df = web.DataReader("UAA", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)

            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="Under Armour Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2018-03-29',
                    y0=10,
                    x1='2018-03-29',
                    y1=25,
                    line=dict(color="black", width=2))
            ])

            return fig, html.A("Under Armour: 150 million records breached on 29th March, 2018",
                               href="https://www.cnbc.com/2018/03/29/under-armour-stock-falls-after-company-admits-data-breach.html")
        elif value == "Marriott":
            start = datetime.datetime(2017, 11, 30)
            end = datetime.datetime(2019, 8, 29)

            df = web.DataReader("UAA", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)

            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="Marriott Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2018-11-30',
                    y0=10,
                    x1='2018-11-30',
                    y1=30,
                    line=dict(color="black", width=2))
            ])

            return fig, html.A("Marriott: 500 million records breached on 30th November, 2018",
                               href="https://www.theguardian.com/world/2018/nov/30/marriott-hotels-data-of-500m-guests-may-have-been-exposed")
        elif value == "EBAY":
            # EBAY	Ebay	EBAY	2014-5-21

            start = datetime.datetime(2013, 5, 21)
            end = datetime.datetime(2015, 5, 21)

            df = web.DataReader("EBAY", 'yahoo', start, end)
            df.reset_index(inplace=True, drop=False)
            df.tail()

            close_px = df['Adj Close']
            mavg_50 = close_px.rolling(window=50).mean()
            mavg_200 = close_px.rolling(window=200).mean()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df['Date'],
                    y=df['Adj Close'],
                    name="EBAY Closing Price",
                    line_color='deepskyblue',
                    opacity=1))

            add_moving_average(df, fig, mavg_50, mavg_200)

            fig.update_layout(shapes=[
                # Line Vertical
                go.layout.Shape(
                    type="line",
                    x0='2014-5-21',
                    y0=15,
                    x1='2014-5-21',
                    y1=32,
                    line=dict(color="black", width=2))
            ])

            return fig, html.A("EBAY: 145 million records breached on 21st May, 2014",
                               href="https://www.washingtonpost.com/news/the-switch/wp/2014/05/21/ebay-asks-145-million-users-to-change-passwords-after-data-breach/")
