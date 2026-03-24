import plotly.graph_objects as go
import pandas as pd

class CompareBarFactory:
    def __init__(self):
        pass

    def make_compare_bar_chart(self, marques, predictions, data_manager):
        # Création du DataFrame pour gérer le tri facilement
        df = pd.DataFrame({
            "Marque": marques, 
            "Prediction": predictions
        })
        
        # Tri par prédiction (croissant pour un bar chart horizontal propre)
        df = df.sort_values(by="Prediction", ascending=True) 

        # Récupération des données triées
        marques_triees = df["Marque"].tolist()
        preds_triees = df["Prediction"].tolist()

        # On demande au data_manager la couleur configurée dans le .ini pour chaque marque triée
        couleurs_triees = [data_manager.get_info(m, "couleur") for m in marques_triees]

        # Génération des labels avec feu si volatilité > 5
        text_labels = [
            f"🔥 {val:.2f} %" if val > 5.0 else f"{val:.2f} %" 
            for val in preds_triees
        ]

        # Construction du graphique
        fig = go.Figure(data=[
            go.Bar(
                y=marques_triees,  
                x=preds_triees,    
                orientation='h',   
                marker=dict(
                    color=couleurs_triees,
                    opacity=0.7, 
                    line=dict(color=couleurs_triees, width=2) 
                ),
                text=text_labels,
                textposition='outside',
                textfont=dict(size=14, color="white"),
                hoverinfo='y+x'
            )
        ])

        fig.update_layout(
            title=dict(
                text="Prédiction de Volatilité (IA)",
                font=dict(color="#FFFFFF", size=20),
                x=0.5
            ),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',  
            font=dict(color='#A0AEC0'),    
            margin=dict(l=20, r=80, t=60, b=20), 
            showlegend=False,              
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='white'),
                gridcolor='rgba(0,0,0,0)' 
            )
        )   
        return fig