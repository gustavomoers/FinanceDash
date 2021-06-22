import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import json

label = ['ambev','klabin','magalu']
value = ['abev3','klbn3','mglu3']


colors = {'header': "rgb(144, 31, 35)",'first_column': 'rgb(190, 195, 218,.2)',
          'column_ttm': 'rgb(248, 181, 0,.3)','head_table':'rgb(190, 195, 218,.5)',
          'receita': 'rgb(144, 31, 35)','custos': 'rgb(61, 174, 254)','bruto' :'rgb(38,38,38)',
          'ebitda':'rgb(133, 204, 254)','ebit':'rgb(98, 112, 167)','lucro':'rgb(248, 181, 0)',
          'contorno':'rgb(8,48,107)'}



styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


ALPHAVANTAGE_API_KEY_1 = '0N9REAL50IN0K66C'

ALPHAVANTAGE_API_KEY_2 = 'LMW3CV85JDLM92I5'

try:

    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY_1, output_format='pandas')
    
except:

    ts = TimeSeries(key=ALPHAVANTAGE_API_KEY_2, output_format='pandas')
    

# dados, meta_dados = ts.get_daily_adjusted(symbol='klbn11.SAO', outputsize='full')
# dados.reset_index(inplace=True)
# dados['date'] = dados['date'].astype('str')






#Dash app layout
app = dash.Dash()
app.title = 'Random'

app.layout = html.Div(
    html.Div([
        html.H1(children='Random nums'),
        html.Div(children='''
            Rand rand rand.
        '''),
        dcc.Store(id='memory-price'),
        
       dcc.Dropdown(
                    id="dropdown_company",
                    options=[{"label": x, "value": y} for x,y in list(zip(label,value))],
                    clearable=False,
                    placeholder="Selecione uma Empresa",
                    style={'font-family':'sans-serif','fontSize':12}),
        
        
        dcc.Graph(id='RandGraph'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ])
    ])
)







# callback for store chosen company price
@app.callback(Output('memory-price', 'data'),
              Input('dropdown_company', 'value'),prevent_initial_call = True)
def price_company(company):

    dados, meta_dados = ts.get_daily_adjusted(symbol='%s.SAO'%company, outputsize='full')
    dados.reset_index(inplace=True)
    dados['date'] = dados['date'].astype('str')
    df_price = dados.to_dict()
    dados = pd.DataFrame(df_price)

    dados['date'] = pd.to_datetime(dados['date'],errors='coerce')
    dados.set_index('date',inplace=True)


    return  [dict(
                x = dados.index,
                y = dados['5. adjusted close'],
                name = 'Preço',
                mode = 'lines', marker = {'color': colors['header']})]






app.clientside_callback(
    """
    function(data) {
        return {
            'data': data,
            'layout': {
                 'xaxis': {'rangeslider_visible': 'True'}
             }
        
        }
    }
    """,
    Output('RandGraph', 'figure'),
    Input('memory-price', 'data')
)


@app.callback(
    Output('relayout-data', 'children'),
    Input('RandGraph', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)



if __name__ == '__main__':
    app.run_server(debug=True)