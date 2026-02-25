# control/control_manager.py
import dash
from dash import callback, Output, Input, State, ctx
import pandas as pd
from dash.exceptions import PreventUpdate

class ControlManager:
    def __init__(self, app, data_manager, view_manager):
        self.app = app
        self.data_manager = data_manager
        self.view_manager = view_manager

    def register_callbacks(self):
        # --- Mise à jour des graphiques dynamiques ---
        @callback(
            Output("dynamic-hist", "figure"),
            Output("dynamic-pie", "figure"),
            Output("hist-legend", "children"),
            Input("column-selector", "value"),
            Input("selected-values", "data"),
        )
        def update_dynamic_graphs(selected_col, selected_values):
            if selected_col is None or selected_values is None:
                raise PreventUpdate

            if selected_col not in selected_values:
                print(f"ERREUR: La clé '{selected_col}' est absente de selected_values")
                raise PreventUpdate

            val = selected_values[selected_col]
            # Appel au ViewManager pour créer les visuels
            hist_fig = self.view_manager.create_histogramme(selected_col, val)
            pie_fig = self.view_manager.create_pie_chart(selected_col)

            descriptions = {
                "Open": "Prix d'ouverture de l'action Tesla.",
                "High": "Prix le plus haut atteint en séance.",
                "Low": "Prix le plus bas atteint en séance.",
                "Close": "Prix de clôture de la journée.",
                "Volume": "Volume d'échanges (titres échangés).",
                "MA_7": "Moyenne mobile sur 7 jours."
            }
            text = descriptions.get(selected_col, f"Analyse de {selected_col}.")
            return hist_fig, pie_fig, text

        # --- Mise à jour du graphique boursier principal ---
        @callback(
            Output("main-stock-chart", "figure"),
            Input("selected-values", "data"),
        )
        def update_main_chart(selected_values):
            return self.view_manager.create_stock_chart()

        # --- Gestion des clics ---
        @callback(
            Output("selected-values", "data"),
            Input("dynamic-hist", "clickData"),
            Input("dynamic-pie", "clickData"),
            Input("main-stock-chart", "clickData"),
            State("column-selector", "value"), 
            State("selected-values", "data"),
            prevent_initial_call=True,
        )
        def update_selected_values(hist_click, pie_click, line_click, current_col, current_data):
            new_vals = current_data.copy()
            triggered_id = ctx.triggered_id
            df_full = self.data_manager.get_full_dataframe()

            if triggered_id == "dynamic-hist" and hist_click:
                new_vals[current_col] = float(hist_click["points"][0]["x"])

            elif triggered_id == "dynamic-pie" and pie_click:
                label_clique = pie_click["points"][0]["label"]
                # Découpage dynamique des catégories
                categories = pd.cut(df_full[current_col], bins=4, labels=["Valeurs de 0 à 125 M", "Valeurs de 125 à 250 M", "Valeurs de 250 à 325 M", "Valeurs de 325 à 500 M"])
                jours = df_full[current_col][categories == label_clique]
                new_vals[current_col] = float(jours.mean())

            elif triggered_id == "main-stock-chart" and line_click:
                date_cliquee = line_click["points"][0]["x"]
                # Recherche de la ligne correspondant à la date cliquée
                ligne = df_full[df_full["Date"] == date_cliquee]
                if not ligne.empty:
                    for col in self.data_manager.get_features_names():
                        new_vals[col] = float(ligne[col].values[0])

            return new_vals

        # --- Prédiction IA ---
        @callback(
            Output("prediction-output", "children"),
            Output("proba-output", "children"),
            Input("selected-values", "data"),
        )
        def update_prediction(selected_values):
            pred = self.data_manager.get_model_prediction(selected_values)
            return f"Estimation de l'agitation (Price Range) : {pred:.2f} $", ""