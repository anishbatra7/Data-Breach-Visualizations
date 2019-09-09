"""Create a Dash app within a Flask app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
from dash import Dash

from .layout import html_layout

df = pd.read_html("https://en.wikipedia.org/wiki/List_of_data_breaches")[0]
converted_records_leaked = pd.to_numeric(df["Records"], errors='coerce')
df['Records'] = converted_records_leaked
df = df[np.isfinite(df['Records'])]

converted_records_year = pd.to_numeric(df["Year"], errors='coerce', downcast='signed')
df['Year'] = converted_records_year
df = df[np.isfinite(df['Year'])]
df['Year'] = df['Year'].astype('int64')

df['Method'].replace('', np.nan, inplace=True)
df.dropna(subset=['Method'], inplace=True)


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
                    routes_pathname_prefix='/dashwiki/')

    # Override the underlying HTML template
    dash_app.index_string = html_layout

    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div(
        [
            html.H2('Data Breach - ML PROJECT'),
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in
                         ['Records lost by Entity', 'Records lost by Method', 'Records lost by Year',
                          'Records lost by Sector']],
                value='Records lost by Year'
            ),
            dcc.Graph(id="graph", style={"width": "100%", "height": "100%", "display": "inline-block"}),
        ]
    )

    # Pass dash_app as a parameter
    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(dash.dependencies.Output('graph', 'figure'),
                       [dash.dependencies.Input('dropdown', 'value')])
    def display_value(value):
        if value == "Records lost by Entity":
            fig = px.scatter(
                df,
                x='Records',
                y='Year',
                range_x=[5000, 3500000000],
                symbol='Organization type',
                animation_group='Organization type',
                color='Organization type',
                hover_name='Entity',
                hover_data=["Method"],
                color_discrete_sequence=px.colors.qualitative.Alphabet,
                log_x=True,
                height=800,
                opacity=1,
                render_mode='webgl',
                width=1400)

            fig.update_traces(
                marker=dict(size=15, line=dict(width=1, color='DarkSlateGrey')),
                selector=dict(mode='markers'))
            return fig
        elif value == "Records lost by Method":
            return go.Figure(data=[go.Pie(labels=df["Method"], values=df["Records"], hole=0.2)])
        elif value == "Records lost by Year":
            return px.bar(
                df,
                x='Year',
                y='Records',
                color='Method',
                hover_data=['Entity'],
                height=800,
                width=1400)
        elif value == 'Records lost by Sector':
            fig_pie = go.Figure(
                data=[go.Pie(labels=df["Organization type"], values=df["Records"])])

            fig_pie.update_traces(
                hoverinfo='label+percent',
                textinfo='value',
                textfont_size=10,
                marker=dict(
                    colors=df["Organization type"], line=dict(color='#000000', width=1.2)))
            return fig_pie
