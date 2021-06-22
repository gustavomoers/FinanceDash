import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import time

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import acoes


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([

            dbc.Navbar([  ##barra de navegação
                        dbc.Row(
                                [
                                    dbc.Col([html.Img(src=app.get_asset_url("logooo.png"), height="35px",)],
                                    width={'size': 4, 'offset': 1}),
                                    dbc.Col([dbc.NavItem(dbc.NavLink("Ações", href="/apps/acoes",
                                    style={'text-align': 'center','font-weight': '200','display': 'inline-block',
                                    'color': 'rgb(12, 11, 11)','white-space': 'nowrap',
                                    'vertical-align': 'middle',
                                    '-webkit-user-select': 'none',
                                    '-moz-user-select': 'none',
                                    '-ms-user-select': 'none',
                                    'user-select': 'none','font-size': '1.0rem','font-weight': '300'}),

                                    style={'height':'35px',
                                    'color': 'rgb(12, 11, 11)',
                                    'background-color': 'rgb(190, 195, 218)',
                                    'border-color': 'rgb(248, 181, 0)',
                                    'display': 'inline-block',
                                    'font-weight': '200',
                                    'text-align': 'center',
                                    'white-space': 'nowrap',
                                    'vertical-align': 'middle',
                                    '-webkit-user-select': 'none',
                                    '-moz-user-select': 'none',
                                    '-ms-user-select': 'none',
                                    'user-select': 'none',
                                    'border': '2px rgb(248, 181, 0) solid',
                                    'padding': '.375rem .75rem',
                                    'font-size': '.8rem',
                                    'line-height': '0.8',
                                    'border-radius': '.25rem'})],
                                    width={'size': 1, 'offset': 5},align='center')  
                                ],
                                
                                no_gutters=True,style={'height':'30px'}
                             ),
                          
                            dbc.NavbarToggler(id="navbar-toggler"),
                        ],
                            color='rgb(144, 31, 35)',
                            dark=True,
                        ),

    ]),
    html.Div(id='page-content', children=[]),
    
    dcc.Loading(
            id="loading-1",
            type="default",
            children=[html.Div([html.Div(id="loading-output-1")])],
        ),
])





@app.callback(Output("loading-output-1", "children"), Input("dre_graph", "value"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/acoes':
        return acoes.layout

    else:
        return acoes.layout


if __name__ == '__main__':
    app.run_server(debug=True)