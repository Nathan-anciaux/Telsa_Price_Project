from dash import html, callback
from dash.dependencies import Input, Output, State

import pandas as pd
from data.data import model
from data.data import feature_names
from data.data import target_names
from view.histogramFactory import make_histogram

# =====================================================
# Update histograms
# =====================================================
@callback(
    [Output(f"hist-{i}", "figure") for i in range(len(feature_names))],
    Input("selected-values", "data"),
)
def update_histograms(selected_values):

    figs = []

    for i, f in enumerate(feature_names):
        val = selected_values[f]
        figs.append(make_histogram(f, val))

    return figs


# =====================================================
# Click handling
# =====================================================
@callback(
    Output("selected-values", "data"),
    [Input(f"hist-{i}", "clickData") for i in range(len(feature_names))],
    State("selected-values", "data"),
    prevent_initial_call=True,
)
def update_selected_values(*args):

    *clicks, current = args

    new_vals = current.copy()

    for i, click in enumerate(clicks):
        if click:
            x = click["points"][0]["x"]
            new_vals[feature_names[i]] = float(x)

    return new_vals


# =====================================================
# Prediction
# =====================================================
@callback(
    Output("prediction-output", "children"),
    Output("proba-output", "children"),
    Input("selected-values", "data"),
)
def update_prediction(selected_values):

    x = [selected_values[f] for f in feature_names]

    X_input = pd.DataFrame([x], columns=feature_names)

    pred = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)[0]

    pred_name = target_names[pred]

    proba_list = html.Ul([
        html.Li(f"{target_names[i]} : {proba[i]:.3f}")
        for i in range(len(target_names))
    ])

    return f"Classe prédite : {pred_name}", proba_list