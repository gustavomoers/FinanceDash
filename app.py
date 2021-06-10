  
import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True, 
                title='FinanceDash',
                external_stylesheets=[dbc.themes.YETI],
                
                )
server = app.server