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
                            html.H4("Sélection des variables"),

                            html.Div(
                                children=[
                                    html.Div(
                                        style={"marginBottom": "40px", "borderBottom": "1px solid #ddd"}, # Un peu de style pour séparer chaque variable
                                        children=[
                                            # histogrammes
                                            dcc.Graph(
                                                id=f"hist-{i}",
                                                config={"displayModeBar": False},
                                            ),

                                            dcc.Graph(
                                                id=f"pie-{i}",
                                                config={"displayModeBar": False},
                                            )
                                        ]
                                    )
                                    for i in range(len(Column_tesla))
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
                                style={"fontSize": "22px", "marginTop": "20px", "fontWeight": "bold", "color": "#CF1717"},
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