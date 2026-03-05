# control/control_manager.py
from dash import callback, Output, Input, State, ctx
from dash.exceptions import PreventUpdate
from configparser import ConfigParser


class ControlManager:
    def __init__(self, app, data_manager, view_manager):
        self.app = app
        self.data_manager = data_manager
        self.view_manager = view_manager

    def register_callbacks(self):
        # enregistre tous les callbacks possibles dans notre site

        @self.app.callback(
            Output('page-content', 'children'),
            Input('url', 'pathname')
        )
        def display_page(pathname):
            # Dictionnaire de correspondance Route -> Nom de la marque
            brands = {
                '/tesla': 'Tesla',
                '/bmw': 'BMW',
                '/lambo': 'Lamborghini',
                '/toyota': 'Toyota'
            }

            if pathname in brands:
                # On appelle la fonction générique avec le nom correct
                return self.view_manager.get_car_page(brands[pathname])
            
            elif pathname == '/compare':
                return html.H1("Page de comparaison (À venir)")
            
            else:
                return self.view_manager.get_home_layout()

        # se declenche des que l'utilisateurs fais une action sur les graphiques
        @callback(
            Output("dynamic-hist", "figure"),
            Output("dynamic-pie", "figure"),
            Output("hist-legend", "children"),
            Input("column-selector", "value"),
            Input("selected-values", "data"),
            Input("active-brand", "data"),
        )

        def update_dynamic_graphs(selected_col, selected_values):
            # si aucune données n'est prete on maj pas pour pas crash 
            # (au lancement du site le dropdown peut envoyer None et ça ferais crash avec le tableau telsa[selected_col])
            if not selected_col or not selected_values or not active_brand:
                raise PreventUpdate

            if selected_col not in selected_values:
                raise PreventUpdate

            val = selected_values[selected_col]
            # Appel au ViewManager pour créer les visuels
            hist_fig = self.view_manager.create_histogramme(selected_col, val, active_brand)
            pie_fig = self.view_manager.create_pie_chart(selected_col, active_brand)

            # les légendes
            descriptions = {
                "Open": "Prix d'ouverture de l'action Tesla.",
                "High": "Prix le plus haut atteint en séance.",
                "Low": "Prix le plus bas atteint en séance.",
                "Close": "Prix de clôture de la journée.",
                "Volume": "Volume d'échanges (titres échangés).",
                "MA_7": "Moyenne mobile sur 7 jours."
            }
            text = descriptions.get(selected_col, f"Analyse de {selected_col} pour {active_brand}.")
            return hist_fig, pie_fig, text

        # affiche le candlestick independemment des autres, pas de selected column
        @callback(
            Output("main-stock-chart", "figure"),
            Input("selected-values", "data"),
            Input("active-brand", "data"),
        )
        def update_main_chart(selected_values):
            return self.view_manager.create_stock_chart()

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
            prevent_initial_call=True, # évite de déclencher au chargement de la page
        )
        def update_selected_values(hist_click, pie_click, line_click, current_col, current_data):
            # on copie pour ne pas modifier sans faire expres
            new_vals = current_data.copy()

            # ctx.triggered_id permet de savoir quel input a declenche le callback
            triggered_id = ctx.triggered_id
            df_full = self.data_manager.get_full_dataframe()

            # clic sur l'histogramme, maj d'une valeur spécifique
            if triggered_id == "dynamic-hist" and hist_click:
                new_vals[current_col] = float(hist_click["points"][0]["x"])

            # clic sur le camembert
            elif triggered_id == "dynamic-pie" and pie_click:
                label_clique = pie_click["points"][0]["label"]
                moyenne = self.data_manager.get_pie_category_mean(current_col, label_clique)
                
                if moyenne is not None:
                    new_vals[current_col] = float(moyenne)
                else:
                    raise PreventUpdate

            # clic que la bourse 
            elif triggered_id == "main-stock-chart" and line_click:
                date_cliquee = line_click["points"][0]["x"]
                features_dict = self.data_manager.get_features_by_date(date_cliquee)
                
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
            pred = self.data_manager.get_model_prediction(selected_values)
            return f"Estimation de l'agitation (Price Range) de {active-brand} : {pred:.2f} $"