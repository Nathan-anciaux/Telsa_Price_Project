from dash import html, callback, dcc, ctx
from dash.dependencies import Input, Output, State

import pandas as pd
# on récupere la data qu'il faut
from data.data import model1
from data.data import Column_tesla

from view.histogramFactory import make_histogram
from view.pieFactory import make_pie_chart
from view.lineChartFactory import make_stock_chart

from data.data import jeux_tesla

# =====================================================
# Update graph
# =====================================================

@callback(
    Output("dynamic-hist", "figure"),
    Output("dynamic-pie", "figure"),
    Output("hist-legend", "children"),
    Input("column-selector", "value"),
    Input("selected-values", "data"),
)

def update_dynamic_graphs(selected_col, selected_values):
    #recupere les données
    val = selected_values[selected_col]
    #on appel les factory pour creer les figures
    hist_fig = make_histogram(selected_col, val)
    pie_fig = make_pie_chart(selected_col)

    descriptions={
        "Open": "Prix d'ouverture de l'action par rapport à l'historique 2010-2025.",
        "High": "Prix le plus haut atteint durant la séance boursière.",
        "Low": "Prix le plus bas atteint durant la séance boursière.",
        "Close": "Prix de clôture (fin de journée) utilisé pour calculer la tendance.",
        "Volume": "Quantité totale de titres Tesla échangés sur le marché ce jour-là.",
        "MA_7": "Moyenne mobile des 7 derniers jours (lissage de la tendance)."
    }

    legend_text = descriptions.get(selected_col, f"Analyse de la variable {selected_col}.")
    text = f"{legend_text}"

    return hist_fig, pie_fig, text


# =====================================================
# Update lineChart
# =====================================================
@callback(
    Output("main-stock-chart", "figure"),
    Input("selected-values", "data"),
)
def update_main_chart(selected_values):
    return make_stock_chart(jeux_tesla)

# =====================================================
# Click handling (Garde UNIQUEMENT ce bloc là)
# =====================================================
@callback(
    Output("selected-values", "data"),
    Input("dynamic-hist", "clickData"), #click sur hist
    Input("dynamic-pie", "clickData"), #click sur pie
    Input("main-stock-chart", "clickData"), #click sur chart
    State("column-selector", "value"), 
    State("selected-values", "data"),
    prevent_initial_call=True,
)

def update_selected_values(hist_click, pie_click, line_click, current_col, current_data):
    new_vals = current_data.copy() #on travaille sur une copie pour eviter les effets de bord
    triggered_id = ctx.triggered_id

    # Clic sur l'histogramme
    if triggered_id == "dynamic-hist" and hist_click:
        #on regarde la valeur sur laxe x (valeur réelle -> prix en $, volume...)
        #que prédit randomforest? si on a x au départ
        new_vals[current_col] = float(hist_click["points"][0]["x"])

    # Clic sur le camembert
    elif triggered_id == "dynamic-pie" and pie_click:
        #bas moyen ou haut
        label_clique = pie_click["points"][0]["label"]
        categories = pd.cut(jeux_tesla[current_col], bins=4, labels=["0 à 125 M", "125 à 250 M", "250 à 375 M","375 à 500 M"])
        #calcule la moyenne des jours appartenant au label
        jours = jeux_tesla[current_col][categories == label_clique]
        new_vals[current_col] = float(jours.mean())

    # Clic sur le graphique boursier
    elif triggered_id == "main-stock-chart" and line_click:
        #recup la date
        date_cliquee = line_click["points"][0]["x"]
        ligne = jeux_tesla[jeux_tesla["Date"] == date_cliquee]
        if not ligne.empty:
            #met a jour toutes les variables d'un coup en fct de la date
            for col in Column_tesla:
                new_vals[col] = float(ligne[col].values[0])

    return new_vals

    # RÉSUME
    # Quand on clique sur un piechart, il prend la moyenne de la catégorie et il place la petite barre dans l'histogramme à cette valeur.

# =====================================================
# Prediction
# =====================================================
@callback(
    Output("prediction-output", "children"),
    Output("proba-output", "children"),
    Input("selected-values", "data"),
)
def update_prediction(selected_values):
    #prépare la liste des caractéristiques pour le model
    x = [selected_values[f] for f in Column_tesla]

    X_input = pd.DataFrame([x], columns=Column_tesla)

    pred = model1.predict(X_input)[0]

    message = f"Estimation Price Range of a market action (agitation): {pred:.2f} $"

    return message, ""