#!/usr/bin/env python
# coding: utf-8

#Importation des librairies requises
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import matplotlib as plt
import plotly.express as px
import pandas as pd

#Création des données à partir du relevé météo
df = pd.read_csv("./donnees-synop-essentielles-omm.csv", sep=';')

#Création de la matrice de corrélation
fig = px.scatter_matrix(df,
         dimensions=["Temperature", "Pnt_rosee", "Humidite", "Hteur_base_nuages"],
         title="Matrice de Corrélation : "
    )

fig2 = px.scatter(
        df,
        x="Temperature", y="Pnt_rosee",
        title="Point de rosée en fonction de la température"
    )

#Création de l'application
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#Visuel de l'application
app.layout = html.Div(className="", children=[
    # Entete
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

    # Contenu
    html.Div(className="body", children=[
        html.H3("Quelques graphiques : "),
        #Premier graphique
        html.Div("On regarde tout d'abord les corrélations entre les variables : "), 
        
        #Emplacement de la matrice
        html.Div(
            dcc.Graph(figure=fig),
        ),
        
        #On saute une ligne
        html.Hr(),
        
        #Deuxième graphique
        html.Div("Sur la matrice seule 4 variables sont disponibles, on peut aussi regarder librement la corrélation entre deux variables quelconques"), 
        html.Div("(Indice : Bonne corrélation Temperature/Point de Rosée et Temperature/Humidité)"), 

        # Ici on veut un graphique simple à deux dimensions, donc deux menus déroulants
        
        dcc.Dropdown(
            id="x-dropdown",
            value="Temperature",
            options=[{"label": name, "value": name} for name in df.columns],
        ),

        dcc.Dropdown(
            id="y-dropdown",
            value="Hteur_base_nuages",
            options=[{"label": name, "value": name} for name in df.columns],
        ),
        
        # Emplacement du graphique
        html.Div(
            dcc.Graph(id='graph'),
        ),
        
        #Troisième graphique
        html.Div("Regardons de plus près le couple Temperature/Point de rosée: "),
        
        #Emplacement du graphique
        html.Div(
            dcc.Graph(figure=fig2),
        ),
        
        #Quelques explications
        html.Div("Merveilleux, on voit que la température et la température sous laquelle la rosée se dépose naturellement sont corrélées, il va falloir expliquer le phénomène : On obtient un graphe similaire aux approximations d'August-Roche-Magnus; Le point de rosée correspond aussi à la température à laquelle la pression partielle de vapeur d'eau est égale à sa pression de vapeur saturante. On peut donc calculer l'humidité grâce au point de rosée.")
        
    ]),

    #Bas de page
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

#Fonctions d'affichage des graphiques

@app.callback(
    Output('graph', 'figure'),
    #On retrouve les deux valeurs des menus déroulants correspondant aux deux dimensions du graphique
    [Input("x-dropdown", "value"),
     Input("y-dropdown", "value")],
)
def display_graph(xvalue, yvalue):
    #On crée le graphique
    figure = px.scatter(
        df,
        x=xvalue, y=yvalue,
    )
    #On retourne le graphique
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
