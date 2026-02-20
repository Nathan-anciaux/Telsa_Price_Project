"""
import plotly.graph_objects as go

import data.data
from data.data import iris_df

# =====================================================
# Histogram helper
# =====================================================

def make_histogram(feature, selected_value):

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=iris_df[feature],
            nbinsx=20,
            opacity=0.7,
        )
    )

    # Selected value
    fig.add_vline(
        x=selected_value,
        line_dash="dash",
        line_width=2,
    )

    fig.update_layout(
        title=feature,
        height=200,
        margin=dict(l=40, r=20, t=40, b=40),
        showlegend=True,
    )

    return fig
"""