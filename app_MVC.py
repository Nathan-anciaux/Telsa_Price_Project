import dash
from dash import html, Input, Output, State, callback

import data.data
import view.layoutManager as view
import control.control
"""
# =====================================================
# App
# =====================================================
app = dash.Dash(__name__)
server = app.server
app.layout = view.layout
"""
# =====================================================
# App
# =====================================================
app = dash.Dash(__name__)
server = app.server

app_dm = DataManager()
app_vm = ViewManager(app_dm)
app.layout = app_vm.get_layout(app_dm)
app_cm = ControlManager(app_dm, app_vm)
app_cm.register_callbacks()

# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)