import plotly.graph_objects as go


class PieFactory:
    def __init__(self):
        self.colors = ["#43A19E", "#5CB8FF", "#F4A261", "#E95A5A"]

    def make_pie_chart(self, feature, data_manager, active_brand):
        labels, values = data_manager.get_pie_chart_data(active_brand, feature)

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.7,
                    marker_colors=self.colors,
                    textinfo="percent",
                    hoverinfo="label+value",
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text=f"Distribution : {feature}", font=dict(color="white", size=16)
            ),
            paper_bgcolor="rgba(0,0,0,0)",  # fond extérieur du graphique invisifble
            plot_bgcolor="rgba(0,0,0,0)",  # fond intérieur invisible
            font=dict(color="#A0AEC0"),  # couleur texte général
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(
                orientation="h",  # légende en bas
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
            ),
        )
        return fig
