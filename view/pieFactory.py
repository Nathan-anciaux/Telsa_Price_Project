import pandas as pd
import plotly.graph_objects as go

class PieFactory:
    def __init__(self):
        self.colors = ["#DFEFFB", "#A2D7FF", "#5CB8FF", "#0091FF"]

    def make_pie_chart(self, feature, data_manager):
        df = data_manager.get_full_dataframe()
        
        # Découpage dynamique des données
        categories = pd.cut(
            df[feature], 
            bins=4, 
            labels=["Tranche 1", "Tranche 2", "Tranche 3", "Tranche 4"]
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