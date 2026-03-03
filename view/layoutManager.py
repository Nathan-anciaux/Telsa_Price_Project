
from dash import dcc, html

# =====================================================
# Layout OO
# =====================================================

class LayoutManager:
    def __init__(self):
        pass
    def get_root_layout(self):
        return html.Div(
            style={"display": "flex", "flexDirection": "column", "minHeight": "100vh"},
            children=[
                dcc.Location(id='url', refresh=False),
                
                # --- Barre de Navigation ---
                html.Nav(
                    style={
                        "backgroundColor": "#1e1e1e", 
                        "padding": "15px 30px", 
                        "display": "flex", 
                        "gap": "30px",
                        "borderBottom": "2px solid #e2212d"
                    },
                    children=[
                        dcc.Link("Accueil", href='/', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Tesla", href='/tesla', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard BMW", href='/bmw', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Lamborghini", href='/lambo', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Toyota", href='/toyota', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Comparateur", href='/compare', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                    ]
                ),
                
                # --- Zone de Contenu Dynamique ---
                # flex: 1 permet à cette zone de pousser le footer vers le bas
                html.Div(id='page-content', style={"padding": "40px", "flex": "1"}),
                
                
            ]
        )
    
    def get_home_layout(self):
        #affichage de la page d'acceuil
        return html.Div([
            html.H1("Analyse de tesla", style={'textAlign': 'center', 'marginTop': '50px'}),
            html.P("Outils de prédiction et d'analyse des actions Tesla au cours du temps.", 
                   style={'textAlign': 'center'}),
            
            # Bouton de navigation
            html.Div([
                dcc.Link(
                    html.Button("Accéder aux données Tesla", id="go-to-data-btn"),
                    href='/dashboard' # Définit la nouvelle URL
                )
            ], style={'textAlign': 'center', 'marginTop': '30px'})
        ])

    def get_brand_layout(self, data_manager, brand_name):
       #GENERE UN DASHBOARD COMPLET POUR CHAQUE VOITURE
        return html.Div(
            style={"padding": "20px"},
            children=[
                # Titre dynamique selon la marque
                html.H2(f"Analyse et Prédiction : Action {brand_name}"),
                html.Hr(),

                dcc.Store(
                    id="selected-values",
                    data=data_manager.get_default_values(),
                ),

                html.Div(
                    style={"display": "flex"},
                    children=[
                        # ================= Left panel (Graphiques) =================
                        html.Div(
                            style={"width": "60%"},
                            children=[
                                dcc.Dropdown(
                                    id="column-selector",
                                    options=[{"label": col, "value": col} for col in data_manager.get_features_names()],
                                    value=data_manager.get_default_feature(),
                                    clearable=False,
                                    style={"marginBottom": "20px"}
                                ),

                                html.Div([
                                    dcc.Graph(id="dynamic-hist", config={"displayModeBar": False}),
                                    html.P(id="hist-legend", style={"textAlign": "center"}),
                                    dcc.Graph(id="dynamic-pie", config={"displayModeBar": False}),
                                ]),

                                dcc.Graph(id="main-stock-chart"),
                            ],
                        ),

                        # ================= Right panel (IA) =================
                        html.Div(
                            style={"width": "40%", "paddingLeft": "30px", "textAlign": "center", "marginTop": "350px"},
                            children=[
                                html.H4(f"Résultat IA {brand_name}"),
                                html.Div(id="prediction-output", style={"fontSize": "22px", "fontWeight": "bold"}),
                                html.Br(),
                                html.Div(id="proba-output", style={"fontSize": "16px"}),
                            ],
                        ),
                    ],
                ),
            ],
        )
    