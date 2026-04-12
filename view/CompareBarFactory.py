import plotly.graph_objects as go


class CompareBarFactory:
    def __init__(self, theme):
        self.theme = theme

    def make_compare_bar_chart(self, marques, predictions, data_manager=None):
        # 1. Couleur de secours dynamique
        if data_manager:
            couleurs = [data_manager.get_info(m, "couleur") for m in marques]
        else:
            couleurs = [self.theme["accent"]] * len(marques)

        warning_threshold = 5.0
        text_labels = [
            f"⚠️ {val:.2f} %" if val > warning_threshold else f"{val:.2f} %"
            for val in predictions
        ]

        valeur_max_fond = max(predictions) * 1.2 if predictions else 10
        fonds_gris = [valeur_max_fond] * len(marques)

        fig = go.Figure()

        # Barres de fond
        fig.add_trace(
            go.Bar(
                x=marques,
                y=fonds_gris,
                marker=dict(color="rgba(255, 255, 255, 0.1)"),
                width=0.45,
                hoverinfo="none",
                showlegend=False,
            )
        )

        # Barres de couleur
        fig.add_trace(
            go.Bar(
                x=marques,
                y=predictions,
                marker=dict(color=couleurs, opacity=0.9),
                width=0.45,
                text=text_labels,
                textposition="inside",
                insidetextanchor="end",
                textfont=dict(size=14, color=self.theme["texte"]),
                hoverinfo="x+y",
                showlegend=False,
            )
        )

        fig.update_layout(
            title=dict(
                text="Model Volatility Prediction",
                font=dict(color=self.theme["texte"], size=20),
                x=0.5,
            ),
            barmode="overlay",
            barcornerradius=20,
            font=dict(color=self.theme["texte_secondaire"]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=60, b=40),
            xaxis=dict(
                showgrid=False,
                showticklabels=True,
                tickfont=dict(size=14, color=self.theme["texte"]),
                zeroline=False,
            ),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        )
        return fig
