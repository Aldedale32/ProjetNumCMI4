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
            id="x1-dropdown",  # identifiant
            value="Temperature",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        dcc.Dropdown(
            id="x2-dropdown",  # identifiant
            value="Pnt_rosee",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        dcc.Dropdown(
            id="x3-dropdown",  # identifiant
            value="Hteur_base_nuages",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        dcc.Dropdown(
            id="x4-dropdown",  # identifiant
            value="Humidite",  # default value
            # all values in the menu
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph'),
        ),
        # a line
        html.Hr(),
        #Second plot
        html.Div("Regardons de plus près le couple Temperature/Point de rosée: "),
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
            value="Pnt_Rosee",
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        # a place for the plot with an id
        html.Div(
            dcc.Graph(id='graph2'),
        ),
        html.Div("Merveilleux, on voit que la température et la température sous laquelle la rosée se dépose naturellement sont corrélées, il va falloir expliquer le phénomène :"),
        html.Hr(),
        html.Hr(),
        html.Div("  -on obtient un graphe similaire aux approximations d'August-Roche-Magnus;"),
        html.Hr(),
        html.Div("  -le point de rosée correspond aussi à la température à laquelle la pression partielle de vapeur d'eau est égale à sa pression de vapeur saturante;"),
        html.Hr(),
        html.Div("  -On peut donc calculer l'humidité grâce au point de rosée.")
        
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
    [Input("x1-dropdown", "value"), Input("x2-dropdown", "value"), Input("x3-dropdown", "value"), Input("x4-dropdown", "value")],
)
def display_graph(x1value, x2value, x3value, x4value):
    figure = pd.plotting.scatter_matrix(
                datsrc[["Temperature","Point_de_rosee","Hauteur_de_la_base_des_nuages","Humidite"]],
                diagonal="kde"
             )

    return figure


@app.callback(
    Output('graph2', 'figure'),
    [Input("x-dropdown", "value"),
     Input("y-dropdown", "value")],
)
def display_graph2(xvalue, yvalue):
    """ 
    This function produce the plot.
    The output is the "figure" of the graph
    The inputs, are the values of the two dropdown menus
    """

    figure = px.scatter(
        df,
        x=xvalue, y=yvalue,
    )

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
