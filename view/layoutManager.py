
from dash import dcc, html

# =====================================================
# Layout OO
# =====================================================

class LayoutManager:
    def __init__(self):
        pass

    def get_layout(self,data_manager):
        return html.Div(
                style={"padding": "20px"},
                children=[
                    html.H2("Prédiction du prix de l'action Tesla"),
                    html.Hr(),

                    dcc.Store(
                        id="selected-values",
                        data=data_manager.get_default_values(),
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
                                        options=[{"label":col, "value":col} for col in data_manager.get_features_names()],
                                        value=data_manager.get_default_feature(),
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
                                        style={"fontSize": "22px", "marginTop": "30px", "fontWeight": "bold", "color": "#000000"},
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
    