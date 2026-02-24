import pandas as pd
import plotly.graph_objects as go
from data.data import jeux_tesla

def make_pie_chart(feature):
    # on divise les données en 3 tranches car données continues : "Bas" "Moyen" "Haut"
    categories = pd.cut(jeux_tesla[feature], bins=4, labels=["0 à 125 M", "125 à 250 M", "250 à 375 M","375 à 500 M"])

    # combien de jours dans chaque tranches
    comptage = categories.value_counts()

    # graph
    fig = go.Figure(data=[
        go.Pie(
            labels=comptage.index, # "Bas" "Moy" "Haut"
            values=comptage.values, # nb jours
            hole=0.4, # fait un trou dans le graph c'est trop stylé
            marker_colors=["#DFEFFB","#A2D7FF", "#5CB8FF", "#0091FF"]
        )
    ])

    fig.update_layout(
        title=f"Répartition {feature}",
        height=200,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True
    )
    return fig
