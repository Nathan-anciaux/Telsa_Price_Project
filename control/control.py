from dash import html, callback, dcc, ctx
from dash.dependencies import Input, Output, State

import pandas as pd
# on récupere la data qu'il faut
from data.data import model1
from data.data import Column_tesla

from view.histogramFactory import make_histogram
from view.pieFactory import make_pie_chart

from data.data import jeux_tesla


# =====================================================
# Update histograms
# =====================================================
@callback(
    [Output(f"hist-{i}", "figure") for i in range(len(Column_tesla))],
    Input("selected-values", "data"),
)
def update_histograms(selected_values):

    figs = []

    for i, f in enumerate(Column_tesla):
        val = selected_values[f]
        figs.append(make_histogram(f, val))

    return figs

# =====================================================
# Update pie charts
# =====================================================
@callback(
    [Output(f"pie-{i}", "figure") for i in range(len(Column_tesla))],
    Input("selected-values", "data"),
)
def update_pie_charts(selected_values):

    figs = []
    
    for f in Column_tesla:
        figs.append(make_pie_chart(f))
        
    return figs

# =====================================================
# Click handling (Hist and Pie)
# =====================================================
@callback(
    Output("selected-values", "data"),
    [Input(f"hist-{i}", "clickData") for i in range(len(Column_tesla))],
    [Input(f"pie-{i}", "clickData") for i in range(len(Column_tesla))],
    State("selected-values", "data"),
    prevent_initial_call=True,
)
def update_selected_values(*args):
    # dash envoie 6 clics hist, 2 clics pie et 1 clic global
    num_cols = len(Column_tesla)
    hist_clicks = args[:num_cols]
    pie_clicks = args[num_cols:2*num_cols]
    current = args[-1]

    new_vals = current.copy()

    # dit quel graph a été cliqué ( ex pie-2)
    triggered_id = ctx.triggered_id

    #sépare "pie" et "2" par ex
    comp_type, idx_str = triggered_id.split("-")
    idx = int(idx_str)
    col_name = Column_tesla[idx]

    # hist part
    if comp_type == "hist":
        click = hist_clicks[idx]
        if click:
            x = click["points"][0]["x"]
            new_vals[col_name] = float(x) # val précise axe X
    
    # pie part
    elif comp_type == "pie":
        click = pie_clicks[idx]
        if click:
            label_clique = click["points"][0]["label"] # recup nom partie cliqué : ex "Bas"
            categories = pd.cut(jeux_tesla[col_name], bins=3, labels=["Bas", "Moyen", "Haut"]) # on re crée les 3 boites pour retrouver les valeurs
            jours_correspondants = jeux_tesla[col_name][categories == label_clique] # on isole les jours qui corresponde à la partie cliqué
            new_vals[col_name] = float(jours_correspondants.mean()) # calc moyenne des jours

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