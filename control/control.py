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
    Input("column-selector", "value"),
    Input("selected-values", "data"),
)

def update_dynamic_graphs(selected_col, selected_values):
    val = selected_values[selected_col]
    hist_fig = make_histogram(selected_col, val)
    pie_fig = make_pie_chart(selected_col)

    return hist_fig, pie_fig


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

    # Clic sur l'histogramme
    if triggered_id == "dynamic-hist" and hist_click:
        new_vals[current_col] = float(hist_click["points"][0]["x"])

    # Clic sur le camembert
    elif triggered_id == "dynamic-pie" and pie_click:
        label_clique = pie_click["points"][0]["label"]
        categories = pd.cut(jeux_tesla[current_col], bins=3, labels=["Bas", "Moyen", "Haut"])
        jours = jeux_tesla[current_col][categories == label_clique]
        new_vals[current_col] = float(jours.mean())

    # Clic sur le graphique boursier
    elif triggered_id == "main-stock-chart" and line_click:
        date_cliquee = line_click["points"][0]["x"]
        ligne = jeux_tesla[jeux_tesla["Date"] == date_cliquee]
        if not ligne.empty:
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

    x = [selected_values[f] for f in Column_tesla]

    X_input = pd.DataFrame([x], columns=Column_tesla)

    pred = model1.predict(X_input)[0]

    message = f"Estimation Price Range: {pred:.2f} $"

    return message, ""