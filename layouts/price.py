import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash_table.Format import Format, Group, Prefix, Scheme, Symbol
import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from dateutil.relativedelta import relativedelta
import json

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
                            dcc.Graph(id="price_graph"),
                        ],width={'size':12, 'offset': 0})
                    ]),

                ])

            ],color="light")

        ])

    ])


def price_graph(on,dados,relOut):

    dados['date'] = pd.to_datetime(dados['date'],errors='coerce')
    dados.set_index('date',inplace=True)

    try: 
        ymin = dados.loc[relOut['xaxis.range'][1]:relOut['xaxis.range'][0],'5. adjusted close'].min()
        ymax = dados.loc[relOut['xaxis.range'][1]:relOut['xaxis.range'][0],'5. adjusted close'].max()
        xrange = relOut['xaxis.range']

    except:
        try:
            ymin = dados.loc[relOut['xaxis.range[1]']:relOut['xaxis.range[0]'],'5. adjusted close'].min()
            ymax = dados.loc[relOut['xaxis.range[1]']:relOut['xaxis.range[0]'],'5. adjusted close'].max()
            xrange = [relOut['xaxis.range[0]'],relOut['xaxis.range[1]']]


        except:

            ymin = dados['5. adjusted close'].min()
            ymax = dados['5. adjusted close'].max()
            xrange = [dados.index.min(),dados.index.max()]
 

            #Graph data
    dataS = [dict(
                    x = dados.index,
                    y = dados['5. adjusted close'],
                    name = 'Preço',
                    mode = 'lines', marker = {'color': colors['header']}
                ),dict(
                    x = dados.index,
                    y = dados['6. volume'],
                    name = 'Volume',type='bar',yaxis= 'y2', marker = {'color': colors['lucro'],'opacity': '.2'}
                )]



                #Graph layout
    layoutS = go.Layout(
                    xaxis=dict(
                        rangeslider_visible=True,
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="1m", step="month", stepmode="backward"),
                                dict(count=6, label="6m", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="1y", step="year", stepmode="backward"),
                                dict(count=5, label="5y", step="year", stepmode="backward"),
                                dict(step="all")
                            ])
                        ),range=xrange,
                    ),
                    yaxis=dict(range=[ymin-2,ymax+2]),
                    yaxis2 = {
                    'overlaying': 'y',
                    'side': 'right'
                }
                )

    return dict(data=dataS,layout=layoutS)


    

 