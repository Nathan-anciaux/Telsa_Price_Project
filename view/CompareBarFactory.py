import plotly.graph_objects as go

class CompareBarFactory:
    def __init__(self):
        self.brand_colors = ["#e82127", "#0066b1", "#d4af37", "#0aeb42"]

    def make_compare_bar_chart(self, marques, predictions):
        text_labels = [f"{val:.2f} %" for val in predictions]

        fig = go.Figure(data=[
            go.Bar(
                x=marques,
                y=predictions,
                marker_color=self.brand_colors,
                text=text_labels,
                textposition='auto', # intérieur ou au-dessus de la barre
                hoverinfo='x+y'
            )
        ])

        fig.update_layout(
            title=dict(
                text="Prédiction IA : Volatilité du jour",
                font=dict(color='white', size=16),
                x=0.5 # centre 
            ),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font=dict(color='#A0AEC0'),    
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,              
            
            
            yaxis=dict(
                title="Volatilité estimée (%)",
                gridcolor='#3a3d60',       
                zerolinecolor='#5CB8FF'    
            ),
            xaxis=dict(
                tickfont=dict(size=14, color='white')
            )
        )   
        return fig