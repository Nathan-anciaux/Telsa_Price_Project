import dash

from data.data_manager import DataManager
from view.view_manager import ViewManager
from control.control_manager import ControlManager
# =====================================================
# App
# =====================================================
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app_dm = DataManager()
app_vm = ViewManager(app_dm)
app.layout = app_vm.get_root_layout()
app_cm = ControlManager(app, app_dm, app_vm)
app_cm.register_callbacks()

# =====================================================
# Run
# =====================================================
if __name__ == "__main__":
    app.run(debug=True, port = 8051)
