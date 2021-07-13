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
from dash.dependencies import Input, Output, State
import json
from app import app

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



@app.callback(Output('price_graph','relayoutData'),
              Input('dropdown_company', 'value'),Input('tabs-styled-with-inline', 'value'), prevent_initial_call=True)

def update_relout(value,one):
    return dict(autosize= True)


#client side implementation
app.clientside_callback(
    """
    function(relOut, Figure) {

        if (typeof relOut !== 'undefined') {
            if (typeof relOut["xaxis.range"] !== 'undefined') {
                //get active filter from graph
                fromS = new Date(relOut["xaxis.range"][0]).getTime()
                toS = new Date(relOut["xaxis.range"][1]).getTime()
                
                xD = Figure.data[0].x
                yD = Figure.data[0].y
                
                //filter y data with graph display
                yFilt = xD.reduce(function (pV,cV,cI){
                    sec = new Date(cV).getTime()
                    if (sec >= fromS && sec <= toS) {
                        pV.push(yD[cI])
                    }
                    return pV
                }, [])
                
                yMax = Math.max.apply(Math, yFilt)
                yMin = Math.min.apply(Math, yFilt)
            } else if (typeof relOut["xaxis.range[0]"] !== 'undefined'){
                //get active filter from graph
                fromS = new Date(relOut["xaxis.range[0]"]).getTime()
                toS = new Date(relOut["xaxis.range[1]"]).getTime()
                
                xD = Figure.data[0].x
                yD = Figure.data[0].y
                
                //filter y data with graph display
                yFilt = xD.reduce(function (pV,cV,cI){
                    sec = new Date(cV).getTime()
                    if (sec >= fromS && sec <= toS) {
                        pV.push(yD[cI])
                    }
                    return pV
                }, [])
                
                yMax = Math.max.apply(Math, yFilt)
                yMin = Math.min.apply(Math, yFilt)


            } else { 
                yMin = Math.min.apply(Math, Figure.data[0].y)
                yMax = Math.max.apply(Math, Figure.data[0].y) 
            }
        } else { 
            yMin = Math.min.apply(Math, Figure.data[0].y)
            yMax = Math.max.apply(Math, Figure.data[0].y) 
        }
        Figure.layout.yaxis = {
            'range': [yMin,yMax],
            'type': 'linear'
        }
   
        return {'data': Figure.data, 'layout': Figure.layout};
    }
    """,
    Output('price_graph','figure'),
    [Input('price_graph','relayoutData'),Input('memory-price', 'data')], prevent_initial_call=True
)
