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
            "texte_secondaire": "#a0aec0",
        }

    def get_root_layout(self, liste_marques):
        # Navigation dynamique
        nav_links = [
            dcc.Link(
                "HomePage", href="/", style={"color": "white", "textDecoration": "none"}
            )
        ]
        for m in liste_marques:
            nav_links.append(
                dcc.Link(
                    f"{m} Dashboard",
                    href=f"/{m.lower()}",
                    style={"color": "white", "textDecoration": "none"},
                )
            )
        nav_links.append(
            dcc.Link(
                "Comparator",
                href="/compare",
                style={"color": "white", "textDecoration": "none"},
            )
        )

        return html.Div(
            style={
                "display": "flex",
                "flexDirection": "column",
                "minHeight": "100vh",
                "backgroundColor": self.theme["fond_page"],
            },
            children=[
                dcc.Location(id="url", refresh=False),
                html.Nav(
                    style={
                        "padding": "15px 30px",
                        "display": "flex",
                        "gap": "30px",
                        "flexWrap": "wrap",
                        "borderBottom": "2px solid #5CB8FF",
                    },
                    children=nav_links,
                ),
                html.Div(id="page-content", style={"padding": "40px", "flex": "1"}),
            ],
        )

    def get_home_layout(self, data_manager):
        marques = data_manager.get_marques()
        return html.Div(
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "padding": "40px 20px",
            },
            children=[
                html.H1(
                    "Stock Market Simulator",
                    style={"color": "white", "fontSize": "48px"},
                ),
                # Grille de cartes générée dynamiquement
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
                        "gap": "25px",
                        "width": "100%",
                        "maxWidth": "1100px",
                    },
                    children=[
                        self._create_brand_card(
                            m, f"/{m.lower()}", data_manager.get_info(m, "logo")
                        )
                        for m in marques
                    ],
                ),
                dcc.Link(
                    href="/compare",
                    style={"textDecoration": "none"},
                    children=html.Div(
                        "Access the Brand Comparison Tool",
                        style={
                            "marginTop": "40px",
                            "padding": "25px",
                            "border": "2px solid #5CB8FF",
                            "borderRadius": "15px",
                            "color": "white",
                        },
                    ),
                ),
            ],
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
            "boxSizing": "border-box",
        }

        return html.Div(
            style={"padding": "10px", "color": self.theme["texte"]},
            children=[
                dcc.Store(id="active-brand", data=brand_name),
                html.H2(f"Analysis and Prediction : {brand_name} Stock - {data_manager.get_info(brand_name, 'description')}"),
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
                            options=[
                                {"label": col, "value": col}
                                for col in data_manager.get_features_names(brand_name)
                            ],
                            value=data_manager.get_default_feature(brand_name),
                            clearable=False,
                        )
                    ],
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
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    style={"flex": "1"},
                                ),
                                html.P(
                                    id="hist-legend",
                                    style={
                                        "textAlign": "center",
                                        "color": self.theme["texte_secondaire"],
                                        "marginTop": "10px",
                                    },
                                ),
                            ],
                        ),
                        # IA
                        html.Div(
                            style={
                                **card_style,
                                "flex": "1",
                                "justifyContent": "center",
                            },
                            children=[
                                html.H4(
                                    f"Model Result (Volatility)",
                                    style={"textAlign": "center", "color": "#FFFFFF"},
                                ),
                                html.Hr(
                                    style={
                                        "borderColor": "#3a3d60",
                                        "width": "80%",
                                        "margin": "10px auto",
                                    }
                                ),
                                html.Div(
                                    id="prediction-output",
                                    style={
                                        "fontSize": "28px",
                                        "fontWeight": "bold",
                                        "textAlign": "center",
                                        "marginTop": "10px",
                                    },
                                ),
                                html.Br(),
                                html.Div(
                                    id="proba-output",
                                    style={
                                        "fontSize": "16px",
                                        "textAlign": "center",
                                        "color": self.theme["texte_secondaire"],
                                    },
                                ),
                            ],
                        ),
                        # pie chart
                        html.Div(
                            style={**card_style, "flex": "1"},
                            children=[
                                dcc.Graph(
                                    id="dynamic-pie", config={"displayModeBar": False}
                                ),
                            ],
                        ),
                    ],
                ),
                # ================= graphique boursier =================
                html.Div(
                    style={"display": "flex", "gap": "20px"},
                    children=[
                        html.Div(
                            style={**card_style, "flex": "1"},
                            children=[
                                dcc.Graph(id="main-stock-chart"),
                            ],
                        ),
                    ],
                ),
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
                    "height": "250px",
                },
                # Ajout d'un effet simple de hover via une classe CSS si tu as un fichier .css,
                # sinon on reste sur du style inline propre.
                children=[
                    html.Img(
                        src=logo_url,
                        style={
                            "height": "100px",
                            "width": "auto",
                            "marginBottom": "20px",
                            "filter": "drop-shadow(0px 0px 5px rgba(255,255,255,0.2))",
                        },
                    ),
                    html.H3(
                        name,
                        style={
                            "color": "white",
                            "margin": "0",
                            "fontSize": "24px",
                            "letterSpacing": "1px",
                        },
                    ),
                    html.Div(
                        "Go →",
                        style={
                            "marginTop": "15px",
                            "fontSize": "12px",
                            "color": "#5CB8FF",
                            "fontWeight": "bold",
                            "textTransform": "uppercase",
                        },
                    ),
                ],
            ),
        )

    def get_compare_layout(self):
        card_style = {
            "backgroundColor": self.theme["fond_carte"],
            "borderRadius": "12px",
            "padding": "20px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.3)",
            "margin": "10px",
        }

        return html.Div(
            [
                html.H2("Comparator", style={"textAlign": "center", "color": "white"}),
                # --- LIGNE DU HAUT ---
                html.Div(
                    style={"display": "flex", "flexWrap": "wrap"},
                    children=[
                        # GAUCHE : Sélecteur de simulation
                        html.Div(
                            style={
                                **card_style,
                                "flex": "1",
                                "minWidth": "300px",
                                "justifyContent": "center",
                            },
                            children=[
                                html.H3(
                                    "Simulation Settings",
                                    style={
                                        "color": "white",
                                        "textAlign": "center",
                                        "marginBottom": "40px",
                                    },
                                ),
                                # --- BLOC OPEN ---
                                html.P(
                                    "Simulate an overall variation in the opening price (Open):",
                                    style={
                                        "color": "white",
                                        "textAlign": "center",
                                        "marginBottom": "40px",
                                    },
                                ),
                                html.Div(
                                    style={
                                        "width": "85%",
                                        "margin": "0 auto",
                                        "paddingBottom": "10px",
                                    },
                                    children=[
                                        dcc.Slider(
                                            id="compare-open-slider",
                                            min=0,
                                            max=2.0,
                                            step=0.01,
                                            value=1.0,
                                            marks={
                                                0: {
                                                    "label": "-100%",
                                                    "style": {"color": "white"},
                                                },
                                                0.5: {
                                                    "label": "-50%",
                                                    "style": {"color": "white"},
                                                },
                                                1.0: {
                                                    "label": "Default",
                                                    "style": {"color": "white"},
                                                },
                                                1.5: {
                                                    "label": "+50%",
                                                    "style": {"color": "white"},
                                                },
                                                2.0: {
                                                    "label": "+100%",
                                                    "style": {"color": "white"},
                                                },
                                            },
                                        )
                                    ],
                                ),
                                html.Div(
                                    id="compare-open-values",
                                    style={"marginBottom": "40px"},
                                ),
                                # --- BLOC VOLUME ---
                                html.P(
                                    "Simulate an overall change in trading volume (Volume):",
                                    style={
                                        "color": "white",
                                        "textAlign": "center",
                                        "marginBottom": "40px",
                                    },
                                ),
                                html.Div(
                                    style={
                                        "width": "85%",
                                        "margin": "0 auto",
                                        "paddingBottom": "10px",
                                    },
                                    children=[
                                        dcc.Slider(
                                            id="compare-volume-slider",
                                             min=0,
                                            max=2.0,
                                            step=0.01,
                                            value=1.0,
                                            marks={
                                                0: {
                                                    "label": "-100%",
                                                    "style": {"color": "white"},
                                                },
                                                0.5: {
                                                    "label": "-50%",
                                                    "style": {"color": "white"},
                                                },
                                                1.0: {
                                                    "label": "Default",
                                                    "style": {"color": "white"},
                                                },
                                                1.5: {
                                                    "label": "+50%",
                                                    "style": {"color": "white"},
                                                },
                                                2.0: {
                                                    "label": "+100%",
                                                    "style": {"color": "white"},
                                                }
                                            },
                                        )
                                    ],
                                ),
                                html.Div(
                                    id="compare-volume-values",
                                    style={"marginBottom": "10px"},
                                ),
                            ],
                        ),
                        # Résultat de l'IA
                        html.Div(
                            style={**card_style, "flex": "1", "minWidth": "300px"},
                            children=[
                                dcc.Graph(
                                    id="compare-ia-bar-chart",
                                    config={"displayModeBar": False},
                                )
                            ],
                        ),
                    ],
                ),
                # --- LIGNE DU BAS ---
                html.Div(
                    style={**card_style},
                    children=[
                        dcc.Graph(
                            id="compare-history-line-chart",
                            config={"displayModeBar": False},
                        )
                    ],
                ),
            ]
        )
