
from dash import dcc, html

# =====================================================
# Layout OO
# =====================================================

class LayoutManager:
    def __init__(self):
        pass
    def get_root_layout(self):
        return html.Div([
            dcc.Location(id='url', refresh=False), # Surveille l'URL
            html.Div(id='page-content')            # Zone où le contenu change
        ])
    
    def get_home_layout(self):
        #affichage de la page d'acceuil
        return html.Div([
            html.H1("Analyse de tesla", style={'textAlign': 'center', 'marginTop': '50px'}),
            html.P("Outils de rédiction et d'analyse des actions Tesla au cours du temps.", 
                   style={'textAlign': 'center'}),
            
            # Bouton de navigation
            html.Div([
                dcc.Link(
                    html.Button("Accéder aux données Tesla", id="go-to-data-btn"),
                    href='/dashboard' # Définit la nouvelle URL
                )
            ], style={'textAlign': 'center', 'marginTop': '30px'})
        ])

    def get_tesla_layout(self,data_manager):
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
    