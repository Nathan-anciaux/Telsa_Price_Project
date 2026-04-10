import plotly.graph_objects as go


class LineChartFactory:
    def make_stock_chart(self, data_manager, active_brand, extra_lines=None):
        # sécurité
        if extra_lines is None:
            extra_lines = {}
        # Récupération du dataframe complet (avec Date, Open, High, etc.)
        df = data_manager.get_full_dataframe(active_brand)

        if "Close" in df.columns:
            col_close = "Close"
        elif "Close/Last" in df.columns:
            col_close = "Close/Last"
        else:
            # En dernier recours, on prend la target définie dans le config.ini
            col_close = data_manager.get_target_names(active_brand)

        fig = go.Figure()

        # Graphique en bougie (Candlestick)
        fig.add_trace(
            go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df[col_close],
                name=f"Prix {active_brand}",
            )
        )

        # Moyenne mobile 7 jours
        for col_name, legend_name in extra_lines.items():
            if col_name in df.columns: # Sécurité
                fig.add_trace(
                    go.Scatter(
                        x=df["Date"],
                        y=df[col_name],
                        mode="lines",
                        name=legend_name,
                        line=dict(width=1.5),
                    )
                )

        fig.update_layout(
            title=dict(text=f"Stock Market History - {active_brand}", font=dict(color="white")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a0aec0"),
            xaxis_rangeslider_visible=True,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig
