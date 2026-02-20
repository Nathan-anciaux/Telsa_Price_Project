"""
from dash import dcc, html

import data.data
from data.data import default_values
from data.data import feature_names


# =====================================================
# Layout
# =====================================================
layout = html.Div(
        style={"padding": "20px"},
        children=[
            html.H2("Prédiction – Random Forest (Iris)"),
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
                            html.H4("Sélection des variables"),

                            html.Div(
                                children=[
                                    dcc.Graph(
                                        id=f"hist-{i}",
                                        config={"displayModeBar": False},
                                    )
                                    for i in range(len(feature_names))
                                ]
                            ),
                        ],
                    ),

                    # ================= Right panel =================
                    html.Div(
                        style={
                            "width": "40%",
                            "paddingLeft": "30px",
                            "textAlign": "center",
                        },
                        children=[
                            html.H4("Résultat"),

                            html.Div(
                                id="prediction-output",
                                style={"fontSize": "22px", "marginTop": "20px"},
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
"""