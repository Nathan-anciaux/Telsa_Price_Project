import plotly.graph_objects as go
import pandas as pd

class CompareBarFactory:
    def __init__(self):
        
        self.brand_colors = {
            "Tesla": "#e82127", 
            "BMW": "#0066b1", 
            "Ferrari": "#d4af37", 
            "Toyota": "#14831f"
        }

    def make_compare_bar_chart(self, marques, predictions):
        
        df = pd.DataFrame({"Marque": marques, "Prediction": predictions})
        
       
        df = df.sort_values(by="Prediction", ascending=True) 

        marques_triees = df["Marque"].tolist()
        preds_triees = df["Prediction"].tolist()

       
        couleurs_triees = [self.brand_colors[m] for m in marques_triees]

       
        text_labels = []
        for val in preds_triees:
            if val > 5.0:
                text_labels.append(f"🔥 {val:.2f} %")
            else:
                text_labels.append(f"{val:.2f} %")

        
        fig = go.Figure(data=[
            go.Bar(
                y=marques_triees,  
                x=preds_triees,    
                orientation='h',   
                marker=dict(
                    color=couleurs_triees,
                    opacity=0.6, 
                    line=dict(color=couleurs_triees, width=3) 
                ),
                text=text_labels,
                textposition='outside',
                textfont=dict(size=16, color="white", family="Arial"),
                hoverinfo='y+x'
            )
        ])

        
        fig.update_layout(
            title=dict(
                text="IA Prediction",
                font=dict(color="#FFFFFF", size=20),
                x=0.5
            ),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font=dict(color='#A0AEC0'),    
            margin=dict(l=20, r=80, t=60, b=20), 
            showlegend=False,              
            
            xaxis=dict(
                title="Volatilité estimée (%)",
                gridcolor='rgba(255, 255, 255, 0.1)', 
                zerolinecolor='#5CB8FF',
                showticklabels=False 
            ),
            yaxis=dict(
                tickfont=dict(size=15, color='white', family="Arial"),
                gridcolor='rgba(0,0,0,0)' 
            )
        )   
        return fig