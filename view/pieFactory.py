import pandas as pd
import plotly.graph_objects as go

class PieFactory:
    def __init__(self):
        self.colors = ["#CFE8FB", "#A2D7FF", "#5CB8FF", "#0091FF"]

    def make_pie_chart(self, feature, data_manager):
        df = data_manager.get_full_dataframe()
        
        # Découpage dynamique des données
        categories = pd.cut(
            df[feature], 
            bins=4, 
            labels=["Valeurs de 0 à 125 M", "Valeurs de 125 à 250 M", "Valeurs de 250 à 325 M", "Valeurs de 325 à 500 M"]
        )

        comptage = categories.value_counts()

        fig = go.Figure(data=[
            go.Pie(
                labels=comptage.index,
                values=comptage.values,
                hole=0.4,
                marker_colors=self.colors
            )
        ])

        fig.update_layout(
            title=f"Répartition {feature}",
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True
        )
        return fig