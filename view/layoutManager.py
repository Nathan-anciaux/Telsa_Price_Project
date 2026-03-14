from dash import dcc, html

# =====================================================
# Layout OO
# =====================================================

class LayoutManager:
    def __init__(self):
        # centraliser les couleurs pour les changer plus facilement 
        self.theme = {
            "fond_page": "#1a1b2f",    
            "fond_carte": "#26294d",   
            "texte": "#ffffff",        
            "texte_secondaire": "#a0aec0" 
        }

    def get_root_layout(self):
        return html.Div(
            style={"display": "flex", "flexDirection": "column", "minHeight": "100vh","backgroundColor": self.theme["fond_page"]},
            children=[
                dcc.Location(id='url', refresh=False),
                
                # --- Barre de Navigation ---
                html.Nav(
                    style={
                        "backgroundColor": "fonc_page", 
                        "padding": "15px 30px", 
                        "display": "flex", 
                        "gap": "30px",
                        "borderBottom": "2px solid #5CB8FF"
                    },
                    children=[
                        dcc.Link("Accueil", href='/', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Tesla", href='/tesla', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard BMW", href='/bmw', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Lamborghini", href='/lambo', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Ferrari", href='/ferrari', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Dashboard Toyota", href='/toyota', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                        dcc.Link("Comparateur", href='/compare', style={"color": "white", "textDecoration": "none", "fontWeight": "bold"}),
                    ]
                ),
                
                # --- Zone de Contenu Dynamique ---
                # permet à cette zone de pousser le footer vers le bas
                html.Div(id='page-content', style={"padding": "40px", "flex": "1"}),
                
                
            ]
        )
    
    def get_home_layout(self):
        #affichage de la page d'acceuil
        return html.Div([
            html.H1("Analyse du marché Automobile", style={'textAlign': 'center', 'marginTop': '50px','color': self.theme['texte']}),
            html.P("Outils de prédiction et d'analyse des actions Automobiles au cours du temps.", 
                   style={'textAlign': 'center','color': self.theme['texte_secondaire']}),
            
            # Bouton de navigation
            html.Div([
                dcc.Link(
                    html.Button("Tesla", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"}, # style de bouton en vrai je kiffe
                    href='/tesla' # Définit la nouvelle URL
                ),
                html.Br(),
                dcc.Link(
                    html.Button("BMW", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"}, # style de bouton en vrai je kiffe
                    href='/bmw' # Définit la nouvelle URL
                ),
                html.Br(),
                dcc.Link(
                    html.Button("Lamborghini", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"}, # style de bouton en vrai je kiffe
                    href='/lambo' # Définit la nouvelle URL
                ),
                html.Br(),
                dcc.Link(
                    html.Button("Ferrari", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"},
                    href='/ferrari' 
                ),
                html.Br(),
                dcc.Link(
                    html.Button("Toyota", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"}, # style de bouton en vrai je kiffe
                    href='/toyota' # Définit la nouvelle URL
                ),
                html.Br(),
                dcc.Link(
                    html.Button("Comparateur", id="go-to-data-btn"),
                    style={"margin": "5px", "padding": "10px 20px", "cursor": "pointer"}, # style de bouton en vrai je kiffe
                    href='/compare' # Définit la nouvelle URL
                ),
            ], style={'textAlign': 'center', 'marginTop': '30px'})
        ])

    def get_brand_layout(self, data_manager, brand_name):
        # GENERE UN DASHBOARD COMPLET POUR CHAQUE VOITURE

        # style de card
        card_style = {
            "backgroundColor": self.theme["fond_carte"],
            "borderRadius": "12px",
            "padding": "20px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.3)",
            "display": "flex",
            "flexDirection": "column",    
            "boxSizing": "border-box"           
        }
       
        return html.Div(
            style={"padding": "10px", "color": self.theme["texte"]},
            children=[
                dcc.Store(id='active-brand', data=brand_name),  
                
                html.H2(f"Analyse et Prédiction : Action {brand_name}"),
                html.Hr(style={"borderColor": "#3a3d60", "marginBottom": "20px"}),

                dcc.Store(
                    id="selected-values",
                    data=data_manager.get_default_values(brand_name),
                ),

                # ================= Menu Déroulant =================
                html.Div(
                    style={"marginBottom": "20px", "color": "black", "width": "30%"}, 
                    children=[
                        dcc.Dropdown(
                            id="column-selector",
                            options=[{"label": col, "value": col} for col in data_manager.get_features_names(brand_name)],
                            value=data_manager.get_default_feature(brand_name),
                            clearable=False,
                        )
                    ]
                ),

                # ================= 3 graphes du haut =================
                html.Div(
                    style={"display": "flex", "gap": "20px", "marginBottom": "20px"},
                    children=[
                        # histogramme
                        html.Div(
                            style={**card_style, "flex": "1 1 0", "minWidth": 0}, 
                            children=[
                                dcc.Graph(
                                    id="dynamic-hist", 
                                    config={"displayModeBar": False, "responsive": True}, 
                                    style={"flex": "1"} 
                                ),
                                html.P(id="hist-legend", style={"textAlign": "center", "color": self.theme["texte_secondaire"], "marginTop": "10px"}),
                            ]
                        ),

                        # IA
                        html.Div(
                            style={
                                **card_style, 
                                "flex": "1", 
                                "justifyContent": "center", 
                            },
                            children=[
                                html.H4(f"Résultat IA (Price Range)", style={"textAlign": "center", "color": "#FFFFFF"}),
                                html.Hr(style={"borderColor": "#3a3d60", "width": "80%", "margin": "10px auto"}),
                                html.Div(id="prediction-output", style={"fontSize": "28px", "fontWeight": "bold", "textAlign": "center", "marginTop": "10px"}),
                                html.Br(),
                                html.Div(id="proba-output", style={"fontSize": "16px", "textAlign": "center", "color": self.theme["texte_secondaire"]}),
                            ]
                        ),

                        # pie chart
                        html.Div(
                            style={**card_style, "flex": "1"}, 
                            children=[
                                dcc.Graph(id="dynamic-pie", config={"displayModeBar": False}),
                            ]
                        ),
                    ]
                ),

                # ================= graphique boursier =================
                html.Div(
                    style={"display": "flex", "gap": "20px"},
                    children=[
                       
                        html.Div(
                            style={**card_style, "flex": "1"}, 
                            children=[
                                dcc.Graph(id="main-stock-chart"),
                            ]
                        ),
                    ]
                )
            ],
        )
    
    def get_compare_layout(self):
        card_style = {
            "backgroundColor": self.theme["fond_carte"],
            "borderRadius": "12px",
            "padding": "20px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.3)",
            "margin": "10px"
        }

        return html.Div([
            html.H2("Laboratoire de Simulation Comparative", style={'textAlign': 'center', 'color': 'white'}),
            
            # --- LIGNE DU HAUT (Sélecteur à gauche, IA à droite) ---
            html.Div(style={"display": "flex", "flexWrap": "wrap"}, children=[
                # GAUCHE : Sélecteur de simulation
                html.Div(style={**card_style, "flex": "1", "minWidth": "300px"}, children=[
                    html.H4("⚙️ Paramètres de Simulation", style={"color": "#5CB8FF"}),
                    html.P("Simulez une variation globale du prix d'ouverture (Open) :"),
                    dcc.Slider(
                        id="compare-open-slider",
                        min=0.8, max=1.2, step=0.01, value=1.0,
                        marks={0.8: '-20%', 1: 'Normal', 1.2: '+20%'},
                    ),
                    html.Br(),
                    html.P("Simulez la nervosité du marché (Volatility_7d) :"),
                    dcc.Slider(
                        id="compare-vol-slider",
                        min=0.5, max=2.0, step=0.1, value=1.0,
                        marks={0.5: 'Calme', 1: 'Normal', 2: 'Crise'},
                    ),
                ]),

                # DROITE : Résultat de l'IA
                html.Div(style={**card_style, "flex": "1", "minWidth": "300px"}, children=[
                    dcc.Graph(id="compare-ia-bar-chart", config={"displayModeBar": False})
                ]),
            ]),

            # --- LIGNE DU BAS (Historique toute largeur) ---
            html.Div(style={**card_style}, children=[
                dcc.Graph(id="compare-history-line-chart", config={"displayModeBar": False})
            ])
        ])