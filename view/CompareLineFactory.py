import plotly.graph_objects as go

class CompareLineFactory:
    def __init__(self):
        self.brand_colors = {
            "Tesla": "#8f171b", 
            "BMW": "#13476d", 
            "Ferrari": "#907211", 
            "Toyota": "#138530"
        }

    def make_compare_line_chart(self, data_manager, marques):
        fig = go.Figure()

        for marque in marques:
            
            df = data_manager.get_full_dataframe(marque)
            df = df.sort_values(by="Date")

            
            premier_prix = df['Open'].iloc[0]
            valeurs_base_100 = (df['Open'] / premier_prix) * 100

            
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=valeurs_base_100,
                mode='lines',
                name=marque,
                line=dict(color=self.brand_colors[marque], width=2)
            ))

        # esthétique
        fig.update_layout(
            title=dict(
                text="Évolution Historique (Base 100)",
                font=dict(color='white', size=16),
                x=0.5
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#A0AEC0'),
            margin=dict(l=20, r=20, t=50, b=20),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.2,
                xanchor="center", x=0.5,
                font=dict(color="white")
            ),
            yaxis=dict(title="Performance (Base 100)", gridcolor='#3a3d60', zerolinecolor='#5CB8FF'),
            xaxis=dict(gridcolor='#3a3d60')
        )   
        return fig