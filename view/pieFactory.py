import pandas as pd
import plotly.graph_objects as go
from data.data import jeux_tesla

def make_pie_chart(feature):
    # on divise les données en 3 tranches car données continues : "Bas" "Moyen" "Haut"
    categories = pd.cut(jeux_tesla[feature], bins=3, labels=["Bas", "Moyen", "Haut"])

    # combien de jours dans chaque tranches
    comptage = categories.value_counts()

    # graph
    fig = go.Figure(data=[
        go.Pie(
            labels=comptage.index, # "Bas" "Moy" "Haut"
            values=comptage.values, # nb jours
            hole=0.4, # fait un trou dans le graph c'est trop stylé
            marker_colors=["#13CFEB", "#220EFF", "#EC71CD"]
        )
    ])

    fig.update_layout(
        title=f"Répartition {feature}",
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True
    )
    return fig
