import plotly.graph_objects as go


class LineChartFactory:
    def make_stock_chart(self, data_manager, active_brand):
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
                name="Prix Tesla",
            )
        )

        # Moyenne mobile 7 jours
        if "MA_7" in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df["MA_7"],
                    mode="lines",
                    name="Moyenne 7j",
                    line=dict(color="orange", width=1.5),
                )
            )

        fig.update_layout(
            title=dict(text=f"Stock Market History", font=dict(color="white")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a0aec0"),
            xaxis_rangeslider_visible=True,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig
