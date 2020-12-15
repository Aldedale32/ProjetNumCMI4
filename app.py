#!/usr/bin/env python
# coding: utf-8

import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import matplotlib as plt
import plotly.express as px
import pandas as pd

# read data file
# ------------------------------------------------------------------------------
df = pd.read_csv("./donnees-synop-essentielles-omm.csv", sep=';')


# Set up app
# ------------------------------------------------------------------------------
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# HTML page Layout
# ------------------------------------------------------------------------------
# Page is divided in three parts:
#    * header: at the top, a title
#    * body: the main containt
#    * footer: at the bottom, contact, informations, credits
app.layout = html.Div(className="", children=[
    # ------ header
    html.Div(
        className="header",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "Relevés météo 2019, station de Tarbes/Ossun",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),

    # ----- body
    html.Div(className="body", children=[
        #First plot
        html.H3("Graphiques : "),
        html.Div("On regarde tout d'abord les corrélations entre les variables"), 
        html.Div("(Indice : Bonne corrélation Temperature/Point de Rosée et Temperature/Humidité)"), 
        # first dropdown selector
        dcc.Dropdown(
            id="x2-dropdown",  # identifiant
            value="Temperature",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph2'),
        ),
        # a line
        html.Hr(),
        html.Div("On peut aussi modéliser en fonction de la date et l'heure ou corréler seulement deux variables: "),
        # first dropdown selector
        dcc.Dropdown(
            id="x-dropdown",  # identifiant
            value="Temperature",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # second dropdown selector
        dcc.Dropdown(
            id="y-dropdown",
            value="Date",
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph'),
        )
    ]),

    # ----- footer
    html.Div(
        className="footer",
        style={"backgroundColor": "#3c6382"},
        children=[html.H2(
            "Copyright Grp 1  M1 CMI",
            style={
                "color": "white",
                "padding": "30px 0 30px 0",
                "textAlign": "center"}
        )],
    ),
])

# Callback functions => interactivity
# Each element on the page is identified thanks to its `id`
# ------------------------------------------------------------------------------


@app.callback(
    Output('graph', 'figure'),
    [Input("x-dropdown", "value"),
     Input("y-dropdown", "value")],
)
def display_graph(xvalue, yvalue):
    """ 
    This function produce the plot.
    The output is the "figure" of the graph
    The inputs, are the values of the two dropdown menus
    """

    figure = px.scatter(
        df,
        x=xvalue, y=yvalue,
        marginal_x="histogram",
        marginal_y="histogram",
        animation_group="Heure",
        template="plotly_white",
    )

    return figure

@app.callback(
    Output('graph2', 'figure2'),
    [Input("x2-dropdown", "value")],
)
def display_graph2(xvalue):
    figure2 = df.plot.scatter(x=xvalue, y="Pnt_rosee")

    return figure2


if __name__ == '__main__':
    app.run_server(debug=True)
