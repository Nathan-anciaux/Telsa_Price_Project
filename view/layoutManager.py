from dash import dcc, html

import data.data
from data.data import default_values
from data.data import Column_tesla


# =====================================================
# Layout
# =====================================================
layout = html.Div(
        style={"padding": "20px"},
        children=[
            html.H2("Prédiction du prix de l'action Tesla"),
            html.Hr(),

            dcc.Store(
                id="selected-values",
                data=default_values,
            ),

            html.Div(
                style={"display": "flex"},
                children=[

                    # ================= Left panel =================
                    html.Div(
                        style={"width": "60%"},
                        children=[
                            
                            #Menu déroulant pour choisir la variable et pas mettre des graphs partout
                            dcc.Dropdown(
                                id="column-selector", #colonne du dataset
                                options=[{"label":col, "value":col} for col in Column_tesla],
                                value=Column_tesla[0],
                                clearable=False, #on vide pas le menu
                                style = {"marginBottom": "20px"}
                            ),

                            #les 2 graphs qui vont changer selon le choix
                            html.Div([
                                dcc.Graph(id="dynamic-hist", config={"displayModeBar": False}),
                                html.P(
                                    id="hist-legend",
                                    style={"fontSize": "15px", "marginTop": "15px", "textAlign": "center"}
                                ),
                                dcc.Graph(id="dynamic-pie", config={"displayModeBar": False}),
                            ]),

                            #graph boursier
                            dcc.Graph(id = "main-stock-chart"),
                        ],
                    ),

                    # ================= Right panel =================
                    html.Div(
                        style={
                            "width": "40%",
                            "paddingLeft": "30px",
                            "textAlign": "center",
                            "marginTop": "350px",
                        },
                        children=[
                            html.H4("Résultat"),

                            html.Div(
                                id="prediction-output",
                                style={"fontSize": "22px", "marginTop": "30px", "fontWeight": "bold", "color": "#CF1717"},
                            ),

                            html.Br(),

                            html.Div(
                                id="proba-output",
                                style={"fontSize": "16px"},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )