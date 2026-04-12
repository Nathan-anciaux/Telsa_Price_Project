import plotly.graph_objects as go

class LineChartFactory:
    def __init__(self, theme):
        self.theme = theme

    def make_stock_chart(self, data_manager, active_brand, extra_lines=None):
        if extra_lines is None:
            extra_lines = {}
            
        df = data_manager.get_full_dataframe(active_brand)

        # --- SÉCURITÉ : Détection de la colonne Close ---
        if "Close" in df.columns:
            col_close = "Close"
        elif "Close/Last" in df.columns:
            col_close = "Close/Last"
        else:
            # Fallback sur la target du config.ini si rien n'est trouvé
            col_close = data_manager.get_target_names(active_brand)

        fig = go.Figure()

        # Graphique en bougies (Candlestick)
        fig.add_trace(
            go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df[col_close], # Utilise la colonne détectée
                name=f"Prix {active_brand}",
            )
        )

        # Lignes supplémentaires (Moyennes mobiles, etc.)
        for col_name, legend_name in extra_lines.items():
            if col_name in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df[col_name],
                        mode="lines",
                        name=legend_name,
                        line=dict(width=1.5)
                    )
                )

        fig.update_layout(
            title=dict(
                text=f"Stock Market History - {active_brand}", 
                font=dict(color=self.theme["texte"])
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color=self.theme["texte_secondaire"], 
                family=self.theme["font_family"]
            ),
            xaxis=dict(gridcolor=self.theme["grille"], rangeslider_visible=True),
            yaxis=dict(gridcolor=self.theme["grille"]),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig