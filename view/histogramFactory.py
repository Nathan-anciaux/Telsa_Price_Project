import plotly.graph_objects as go

# =====================================================
# Histogram helper
# =====================================================


class HistogramFactory:
    def __init__(self, theme):
        self.theme = theme

    def make_histogram(self, feature, selected_value, data_manager, active_brand):
        df = data_manager.get_full_dataframe(active_brand)
        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=df[feature],
                nbinsx=20,
                opacity=0.7,
                marker_color=self.theme["accent"],  # Dynamique
            )
        )

        fig.add_vline(
            x=selected_value,
            line_dash="dash",
            line_width=2,
            line_color=self.theme["texte"],  # Dynamique
        )

        fig.update_layout(
            title=dict(
                text=f"Distribution : {feature}", font=dict(color=self.theme["texte"])
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=self.theme["texte_secondaire"], family=self.theme["font_family"]
            ),
            margin=dict(l=40, r=20, t=40, b=40),
        )
        return fig
