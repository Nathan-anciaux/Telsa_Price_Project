import plotly.graph_objects as go


class CompareLineFactory:
    def __init__(self):
        # On récupère tout dynamiquement via le data_manager dans la méthode ci-dessous.
        pass

    def make_compare_line_chart(self, data_manager, marques):
        fig = go.Figure()

        for marque in marques:
            # Récupération des données via le manager
            df = data_manager.get_full_dataframe(marque)
            df = df.sort_values(by="Date")

            # Récupération de la couleur configurée dans le config.ini
            # On utilise une couleur par défaut (#ffffff) au cas où elle manque
            couleur_marque = data_manager.get_info(marque, "couleur")

            # Calcul de la performance (Base 100)
            # Formule : (Prix actuel / Prix initial) * 100
            premier_prix = df["Open"].iloc[0]
            valeurs_base_100 = (df["Open"] / premier_prix) * 100

            # Ajout de la courbe
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=valeurs_base_100,
                    mode="lines",
                    name=marque,
                    # Utilisation de la couleur dynamique
                    line=dict(color=couleur_marque, width=2),
                    hovertemplate=f"<b>{marque}</b><br>Perf: %{{y:.2f}}%<extra></extra>",
                )
            )

        fig.update_layout(
            title=dict(
                text="Performance Historique Comparée (Base 100)",
                font=dict(color="white", size=18),
                x=0.5,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#A0AEC0"),
            margin=dict(l=40, r=20, t=60, b=40),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(color="white"),
            ),
            yaxis=dict(
                title="Performance indexée",
                gridcolor="#3a3d60",
                zerolinecolor="#5CB8FF",
                ticksuffix="%",
            ),
            xaxis=dict(gridcolor="#3a3d60"),
        )
        return fig
