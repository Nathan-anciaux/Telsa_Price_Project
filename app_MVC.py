import dash
from dash import html, Input, Output, State, callback

import data.data
import view.layoutManager as view
import control.control

# =====================================================
# App
# =====================================================
app = dash.Dash(__name__)
server = app.server
app.layout = view.layout

# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)