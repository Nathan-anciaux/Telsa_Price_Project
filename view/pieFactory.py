import plotly.graph_objects as go

class PieFactory:
    def __init__(self):
        self.colors = ["#CFE8FB", "#A2D7FF", "#5CB8FF", "#0091FF"]

    def make_pie_chart(self, feature, data_manager):
        labels, values = data_manager.get_pie_chart_data(feature)

        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
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