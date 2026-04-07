# control/control_manager.py
from dash import callback, Output, Input, State, ctx, html
from dash.exceptions import PreventUpdate
from configparser import ConfigParser


class ControlManager:
    def __init__(self, app, data_manager, view_manager):
        self.app = app
        self.data_manager = data_manager
        self.view_manager = view_manager

    def register_callbacks(self):
        # enregistre tous les callbacks possibles dans notre site

        @self.app.callback(Output("page-content", "children"), Input("url", "pathname"))
        def display_page(pathname):
            marques = self.data_manager.get_marques()
            # On crée un mapping dynamique { '/tesla': 'Tesla', ... }
            mapping = {f"/{m.lower()}": m for m in marques}

            if pathname == "/":
                return self.view_manager.get_home_layout()
            elif pathname == "/compare":
                return self.view_manager.get_compare_layout()
            elif pathname in mapping:
                return self.view_manager.get_car_page(mapping[pathname])
            return html.H1("404 - Page non trouvée")

        # se declenche des que l'utilisateurs fais une action sur les graphiques
        @callback(
            Output("dynamic-hist", "figure"),
            Output("dynamic-pie", "figure"),
            Output("hist-legend", "children"),
            Input("column-selector", "value"),
            Input("selected-values", "data"),
            Input("active-brand", "data"),
        )
        def update_dynamic_graphs(selected_col, selected_values, active_brand):
            # si aucune données n'est prete on maj pas pour pas crash
            # (au lancement du site le dropdown peut envoyer None et ça ferais crash avec le tableau telsa[selected_col])
            if not selected_col or not selected_values or not active_brand:
                raise PreventUpdate

            if selected_col not in selected_values:
                raise PreventUpdate

            val = selected_values[selected_col]
            # Appel au ViewManager pour créer les visuels
            hist_fig = self.view_manager.create_histogramme(
                selected_col, val, active_brand
            )
            pie_fig = self.view_manager.create_pie_chart(selected_col, active_brand)

            # les légendes
            descriptions = {
                "Open": "Opening price for the day",
                "High": "Highest price reached during the trading session",
                "Low": "Lowest price reached during the session",
                "Close": "Closing price for the day",
                "Volume": "Trading volume (securities traded).",
                "MA_7": "7-day moving average",
            }
            text = descriptions.get(
                selected_col, f"Analysis of {selected_col} for {active_brand}."
            )
            return hist_fig, pie_fig, text

        # affiche le candlestick independemment des autres, pas de selected column
        @callback(
            Output("main-stock-chart", "figure"),
            Input("selected-values", "data"),
            Input("active-brand", "data"),
        )
        def update_main_chart(selected_values, active_brand):
            return self.view_manager.create_stock_chart(active_brand)

        # gestion des clics
        # regarde quel graphique a été cliqué et met a jour le Store
        @callback(
            Output("selected-values", "data"),
            Input("dynamic-hist", "clickData"),
            Input("dynamic-pie", "clickData"),
            Input("main-stock-chart", "clickData"),
            State("column-selector", "value"),
            State("selected-values", "data"),
            State("active-brand", "data"),
            prevent_initial_call=True,  # évite de déclencher au chargement de la page
        )
        def update_selected_values(
            hist_click, pie_click, line_click, current_col, current_data, active_brand
        ):
            # on copie pour ne pas modifier sans faire expres
            if current_data is None or active_brand is None:
                new_vals = {}
            else:
                new_vals = current_data.copy()

            # ctx.triggered_id permet de savoir quel input a declenche le callback
            triggered_id = ctx.triggered_id

            # clic sur l'histogramme, maj d'une valeur spécifique
            if triggered_id == "dynamic-hist" and hist_click:
                new_vals[current_col] = float(hist_click["points"][0]["x"])

            # clic sur le camembert
            elif triggered_id == "dynamic-pie" and pie_click:
                label_clique = pie_click["points"][0]["label"]
                moyenne = self.data_manager.get_pie_category_mean(
                    active_brand, current_col, label_clique
                )

                if moyenne is not None:
                    new_vals[current_col] = float(moyenne)
                else:
                    raise PreventUpdate

            # clic que la bourse
            elif triggered_id == "main-stock-chart" and line_click:
                date_cliquee = line_click["points"][0]["x"]
                features_dict = self.data_manager.get_features_by_date(
                    active_brand, date_cliquee
                )

                if features_dict:
                    for col, val in features_dict.items():
                        new_vals[col] = float(val)

            return new_vals

        # Prediction
        # reagit au changement de données pour recalculer le modele
        @callback(
            Output("prediction-output", "children"),
            Input("selected-values", "data"),
            Input("active-brand", "data"),
        )
        def update_prediction(selected_values, active_brand):
            if not selected_values or not active_brand:
                raise PreventUpdate
            pred = self.data_manager.get_model_prediction(active_brand, selected_values)
            return f"{pred:.2f} %"

        # --- CALLBACK DU COMPARATEUR IA ---
        @self.app.callback(
            Output("compare-ia-bar-chart", "figure"),
            Output("compare-open-values", "children"),
            Output("compare-volume-values", "children"),
            Input("url", "pathname"),
            Input("compare-open-slider", "value"),
            Input("compare-volume-slider", "value"),
        )
        def update_compare_ia(pathname, open_mult, volume_mult):
            if pathname != "/compare":
                raise PreventUpdate

            # Sécurité anti-crash au chargement
            if open_mult is None or volume_mult is None:
                raise PreventUpdate

            marques = self.data_manager.get_marques()
            predictions = []
            open_displays = []
            volume_displays = []

            for marque in marques:
                valeurs = self.data_manager.get_default_values(marque).copy()

                # --- CALCULES OPEN ---
                new_open = valeurs["Open"] * open_mult
                valeurs["Open"] = new_open

                badge_open = html.Span(
                    f"{marque}: {new_open:.1f}",
                    style={
                        "backgroundColor": "#3a3d60",
                        "padding": "4px 8px",
                        "borderRadius": "4px",
                        "fontSize": "12px",
                        "color": "#5CB8FF",
                    },
                )
                open_displays.append(badge_open)

                # --- CALCULES VOLUME ---
                if "Volume" in valeurs:
                    new_volume = valeurs["Volume"] * volume_mult
                    valeurs["Volume"] = new_volume
                    volume_formate = f"{int(new_volume):,}".replace(",", " ")

                    badge_volume = html.Span(
                        f"{marque}: {volume_formate}",
                        style={
                            "backgroundColor": "#3a3d60",
                            "padding": "4px 8px",
                            "borderRadius": "4px",
                            "fontSize": "12px",
                            "color": "#5CB8FF",
                        },
                    )
                    volume_displays.append(badge_volume)

                # --- PRÉDICTION ---
                pred = self.data_manager.get_model_prediction(marque, valeurs)
                predictions.append(pred)

            fig = self.view_manager.create_compare_bar_chart(marques, predictions)

            # Mise en page des badges
            div_open = html.Div(
                open_displays,
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "center",
                    "gap": "8px",
                },
            )
            div_volume = html.Div(
                volume_displays,
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "justifyContent": "center",
                    "gap": "8px",
                },
            )

            return fig, div_open, div_volume

        @self.app.callback(
            Output("compare-history-line-chart", "figure"), Input("url", "pathname")
        )
        def update_compare_history(pathname):
            if pathname != "/compare":
                raise PreventUpdate

            marques = self.data_manager.get_marques()
            return self.view_manager.create_compare_line_chart(marques)
