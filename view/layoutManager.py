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

        brand_data = [
            {"name": "Tesla", "path": "/tesla", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Tesla_logo.png"},
            {"name": "BMW", "path": "/bmw", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg"},
            {"name": "Ferrari", "path": "/ferrari", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Deus_Ferrari.png"},
            {"name": "Toyota", "path": "/toyota", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Toyota_logo_%28Red%29.svg"},
        ]

        return html.Div(
            style={
                "display": "flex", 
                "flexDirection": "column", 
                "alignItems": "center", 
                "justifyContent": "center",
                "padding": "40px 20px"
            },
            children=[
                # --- En-tête ---
                html.Div(
                    style={"textAlign": "center", "marginBottom": "50px"},
                    children=[
                        html.H1("Simuler le marché boursier automobile", 
                                style={"fontSize": "48px", "fontWeight": "800", "color": "white", "marginBottom": "10px"}),
                    ]
                ),

                # --- Grille de Marques ---
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
                        "gap": "25px",
                        "width": "100%",
                        "maxWidth": "1100px"
                    },
                    children=[self._create_brand_card(b["name"], b["path"], b["logo"]) for b in brand_data]
                ),

                # --- Section Comparateur (Lien Large) ---
                dcc.Link(
                    href="/compare",
                    style={"textDecoration": "none", "marginTop": "40px", "width": "100%", "maxWidth": "1100px"},
                    children=html.Div(
                        style={
                            "backgroundColor": "#2d3748", # Une couleur légèrement différente pour se démarquer
                            "borderRadius": "15px",
                            "padding": "25px",
                            "textAlign": "center",
                            "border": "1px dashed #5CB8FF",
                            "transition": "all 0.3s"
                        },
                        children=[
                            html.H3("Accéder au Comparateur de marques", 
                                   style={"color": "#5CB8FF", "margin": "0", "fontSize": "20px"}),
                            html.P("Simulez des variations de marché sur des marques de voitures.",
                                   style={"color": "white", "margin": "5px 0 0 0", "fontSize": "14px", "opacity": "0.7"})
                        ]
                    )
                )
            ]
        )

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
    
    def _create_brand_card(self, name, href, logo_url):
        return dcc.Link(
            href=href,
            style={"textDecoration": "none"},
            children=html.Div(
                style={
                    "backgroundColor": self.theme["fond_carte"],
                    "borderRadius": "20px",
                    "padding": "40px 20px",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "border": "1px solid #3a3d60",
                    "transition": "transform 0.3s, border-color 0.3s, box-shadow 0.3s",
                    "cursor": "pointer",
                    "height": "250px"
                },
                # Ajout d'un effet simple de hover via une classe CSS si tu as un fichier .css, 
                # sinon on reste sur du style inline propre.
                children=[
                    html.Img(src=logo_url, style={"height": "100px", "width": "auto", "marginBottom": "20px", "filter": "drop-shadow(0px 0px 5px rgba(255,255,255,0.2))"}),
                    html.H3(name, style={"color": "white", "margin": "0", "fontSize": "24px", "letterSpacing": "1px"}),
                    html.Div(
                        "Y aller →", 
                        style={"marginTop": "15px", "fontSize": "12px", "color": "#5CB8FF", "fontWeight": "bold", "textTransform": "uppercase"}
                    )
                ]
            )
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
            html.H2("Comparateur", style={'textAlign': 'center', 'color': 'white'}),
            
            # --- LIGNE DU HAUT ---
            html.Div(style={"display": "flex", "flexWrap": "wrap"}, children=[
                # GAUCHE : Sélecteur de simulation
                html.Div(style={**card_style, "flex": "1", "minWidth": "300px", "justifyContent": "center"}, children=[
                    html.H3("Paramètres de Simulation", style={"color": "white", "textAlign": "center", "marginBottom": "40px"}),
                    
                    # --- BLOC OPEN ---
                    html.P("Simulez une variation globale du prix d'ouverture (Open) :", 
                           style={"color": "white", "textAlign": "center", "marginBottom": "40px"}), 
                    html.Div(
                        style={"width": "85%", "margin": "0 auto", "paddingBottom": "10px"},
                        children=[
                            dcc.Slider(
                                id="compare-open-slider",
                                min=0.5, max=3.0, step=0.01, value=1.0,
                                marks={
                                    0.5: {'label': '-50%', 'style': {'color': 'white'}},
                                    1.0: {'label': 'Normal', 'style': {'color': 'white'}},
                                    3.0: {'label': '+200%', 'style': {'color': 'white'}}
                                },
                            )
                        ]
                    ),
                    html.Div(id="compare-open-values", style={"marginBottom": "40px"}), 
                    
                    # --- BLOC VOLUME ---
                    html.P("Simulez une variation globale du volume d'échanges (Volume) :", 
                           style={"color": "white", "textAlign": "center", "marginBottom": "40px"}), 
                    html.Div(
                        style={"width": "85%", "margin": "0 auto", "paddingBottom": "10px"},
                        children=[
                            dcc.Slider(
                                id="compare-volume-slider",
                                min=0.5, max=2.0, step=0.1, value=1.0,
                                marks={
                                    0.5: {'label': '-50%', 'style': {'color': 'white'}},
                                    1.0: {'label': 'Normal', 'style': {'color': 'white'}},
                                    2.0: {'label': '+100%', 'style': {'color': 'white'}}
                                },
                            )
                        ]
                    ),
                    html.Div(id="compare-volume-values", style={"marginBottom": "10px"}),
                ]),

                # Résultat de l'IA
                html.Div(style={**card_style, "flex": "1", "minWidth": "300px"}, children=[
                    dcc.Graph(id="compare-ia-bar-chart", config={"displayModeBar": False})
                ]),
            ]),

            # --- LIGNE DU BAS ---
            html.Div(style={**card_style}, children=[
                dcc.Graph(id="compare-history-line-chart", config={"displayModeBar": False})
            ])
        ])