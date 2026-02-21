import plotly.graph_objects as go

from data.data import jeux_tesla

# =====================================================
# Histogram helper
# =====================================================

def make_histogram(feature, selected_value):

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=jeux_tesla[feature],
            nbinsx=20,
            opacity=0.7,
            marker_color = "#CF1717"
        )
    )

    # Selected value
    fig.add_vline(
        x=selected_value,
        line_dash="dash",
        line_width=2,
        line_color = "red"
    )

    fig.update_layout(
        title=feature,
        height=200,
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=False,
    )

    return fig
