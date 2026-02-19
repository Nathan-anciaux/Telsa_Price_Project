from dash import html, callback
from dash.dependencies import Input, Output, State

import pandas as pd
# on récupere la data qu'il faut
from data.data import model1
from data.data import Column_tesla

from view.histogramFactory import make_histogram

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
# Click handling
# =====================================================
@callback(
    Output("selected-values", "data"),
    [Input(f"hist-{i}", "clickData") for i in range(len(Column_tesla))],
    State("selected-values", "data"),
    prevent_initial_call=True,
)
def update_selected_values(*args):

    *clicks, current = args

    new_vals = current.copy()

    for i, click in enumerate(clicks):
        if click:
            x = click["points"][0]["x"]
            new_vals[Column_tesla[i]] = float(x)

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

    x = [selected_values[f] for f in Column_tesla]

    X_input = pd.DataFrame([x], columns=Column_tesla)

    pred = model1.predict(X_input)[0]

    message = f"Estimation Price Range: {pred:.2f} $"

    return message, ""