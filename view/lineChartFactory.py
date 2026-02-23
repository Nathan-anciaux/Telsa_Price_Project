import plotly.graph_objects as go

def make_stock_chart(df):
    fig = go.Figure()
    #graph en bougie avec tous les prix
    fig.add_trace(go.Candlestick(
        x=df["Date"], open = df["Open"], high = df["High"],
        low=df["Low"], close = df["Close"], name="Prix"
    ))

    #on ajoute la moyenne (trait principal)
    fig.add_trace(go.Scatter(
        x=df["Date"], y = df["MA_7"], mode="lines",
        name="Moyenne 7j", line=dict(color = "orange")
    ))

    fig.update_layout(template= "plotly_dark", xaxis_rangeslider_visible=True)
    return fig