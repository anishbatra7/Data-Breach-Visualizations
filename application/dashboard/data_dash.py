from pathlib import Path

import dash_html_components as html
import dash_table
import pandas as pd
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
                    routes_pathname_prefix='/dashapp/')

    # Override the underlying HTML template
    dash_app.index_string = html_layout

    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div(
        children=get_datasets(),
        id='dash-container'
    )

    return dash_app.server


def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    p = Path('.')
    data_filepath = list(p.glob('data/*.csv'))
    arr = ['']

    for index, csv in enumerate(data_filepath):

        df = pd.read_csv(data_filepath[index], header=0, sep=';')

        file_name = str(data_filepath[index]).split("/")

        if str(data_filepath[index]) == "data/Kaggle.csv":
            arr.append(html.A(html.H1("Kaggle Data", style={'textAlign': 'center', 'color': '#000000'}),
                              href='/dashkaggle/'))
        else:
            arr.append(html.A(html.H1("Realtime Wikipedia Data", style={'textAlign': 'center', 'color': '#000000'}),
                              href='/dashwiki/'))

        table_preview = dash_table.DataTable(
            id='table_' + str(index),
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows"),
            sort_action="native",
            sort_mode='single',
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(0,0,0)',
                'color': 'white'
            },
            page_size=10,
        )

        arr.append(table_preview)

    return arr
