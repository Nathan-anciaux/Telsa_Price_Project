import plotly.graph_objects as go


class PieFactory:
    def __init__(self, theme):
        self.theme = theme
        # On peut même créer une palette dérivée de l'accent
        self.colors = [self.theme["accent"], "#43A19E", "#F4A261", "#E95A5A"]

    def make_pie_chart(self, feature, data_manager, active_brand):
        labels, values = data_manager.get_pie_chart_data(active_brand, feature)
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.7,
                    marker_colors=self.colors,
                    textfont=dict(color=self.theme["texte"]),
                )
            ]
        )

        fig.update_layout(
            title=dict(
                text=f"Propriétés : {feature}", font=dict(color=self.theme["texte"])
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=self.theme["texte_secondaire"], family=self.theme["font_family"]
            ),
            legend=dict(font=dict(color=self.theme["texte"])),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig
