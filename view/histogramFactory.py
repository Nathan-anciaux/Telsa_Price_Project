import plotly.graph_objects as go

# =====================================================
# Histogram helper
# =====================================================

class HistogramFactory:
    def __init__(self):
        # On peut définir des couleurs par défaut ici
        self.bar_color = "#43A19E"
        self.line_color = "white"

    def make_histogram(self, feature, selected_value, data_manager, active_brand):
        # On récupère les données via le data_manager
        df = data_manager.get_full_dataframe(active_brand)
        
        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=df[feature],
                nbinsx=20,
                opacity=0.7,
                marker_color=self.bar_color
            )
        )

        # Selected value curseur
        fig.add_vline(
            x=selected_value,
            line_dash="dash",
            line_width=2,
            line_color=self.line_color
        )

        fig.update_layout(
            title=dict(
                text=f"Distribution : {feature}",
                font=dict(color='white')
            ),
            margin=dict(l=40, r=20, t=40, b=40),
            showlegend=False,
            
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font=dict(color='#a0aec0')
        )

        return fig