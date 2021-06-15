import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
from dash_table.Format import Format, Group, Prefix, Scheme, Symbol
import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import pandas as pd
import pathlib
from dateutil.relativedelta import relativedelta

this_year = datetime.datetime.today().strftime('%Y')
five_yrs_ago = (datetime.datetime.now() - relativedelta(years=5)).strftime('%Y')
today = datetime.datetime.today().strftime('%Y-%m-%d')







colors = {'header': "rgb(144, 31, 35)",'first_column': 'rgb(190, 195, 218,.2)',
          'column_ttm': 'rgb(248, 181, 0,.3)','head_table':'rgb(190, 195, 218,.5)',
          'receita': 'rgb(144, 31, 35)','custos': 'rgb(61, 174, 254)','bruto' :'rgb(38,38,38)',
          'ebitda':'rgb(133, 204, 254)','ebit':'rgb(98, 112, 167)','lucro':'rgb(248, 181, 0)',
          'contorno':'rgb(8,48,107)'}


def layout_tab2():
    return html.Div([
        
        dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            daq.BooleanSwitch(
                                id='price-boolean-switch',
                                on=False,
                                label="Mostrar Volume",
                                labelPosition="bottom",
                                persistence=True,
                                persistence_type='session'
                             ),
                        ],width={'size':2, 'offset': 10})
                    ]),

                    html.Br(),

                    dbc.Row([
                        dbc.Col([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=[dcc.Graph(id="price_graph")]
                            ),
                        ],width={'size':12, 'offset': 0})
                    ]),

                ])

            ],color="light")

        ])

    ])


def price_graph(on,dados):

    try:

        dados['date'] = pd.to_datetime(dados['date'],errors='coerce')
        dados.set_index('date',inplace=True)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_scattergl(name='Preço',x = dados.index, y=dados['5. adjusted close'],secondary_y=False,
            marker_color=colors['header'])
        
        if (on):
            
            fig.add_bar(name='Volume',x = dados.index, y=dados['6. volume'],secondary_y=True,
                marker_color=colors['lucro'],opacity=.9)

        if dados.index.min() < (datetime.datetime.now() - relativedelta(years=5)):
            
            fig.update_xaxes(range=[five_yrs_ago,today])
        
        # Add range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=5,
                            label="5y",
                            step="year",
                            stepmode="backward"),
                        dict(count=3,
                            label="3y",
                            step="year",
                            stepmode="backward"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        return fig
    
    except:
        return 'Não Disponível'