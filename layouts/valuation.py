import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Group, Prefix, Scheme, Symbol
import datetime
import numpy as np
import plotly.graph_objects as go
import re
import pandas as pd
import pathlib
from dateutil.relativedelta import relativedelta

this_year = datetime.datetime.today().strftime('%Y')
five_yrs_ago = (datetime.datetime.now() - relativedelta(years=5)).strftime('%Y')





class Medias:
    # get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../DADOS").resolve()
    setor = pd.read_pickle(DATA_PATH.joinpath('medias_setor.pkl'))
    subsetor = pd.read_pickle(DATA_PATH.joinpath('medias_subsetor.pkl'))
    segmento = pd.read_pickle(DATA_PATH.joinpath('medias_segmento.pkl'))
    mercado = pd.read_pickle(DATA_PATH.joinpath('medias_mercado_ttm.pkl'))
    capital = pd.read_pickle(DATA_PATH.joinpath('medias_capital.pkl'))


colors = {'header': "rgb(144, 31, 35)",'first_column': 'rgb(190, 195, 218,.2)',
          'column_ttm': 'rgb(248, 181, 0,.3)','head_table':'rgb(190, 195, 218,.5)',
          'receita': 'rgb(144, 31, 35)','custos': 'rgb(61, 174, 254)','bruto' :'rgb(38,38,38)',
          'ebitda':'rgb(133, 204, 254)','ebit':'rgb(98, 112, 167)','lucro':'rgb(248, 181, 0)',
          'contorno':'rgb(8,48,107)'}

indicadores = [ 'beta','Média Crescimento Receitas 5 anos','Cost of Capital','Cost of Debt',
              'IC ratio','Cost of Equity','CAGR Receita 5 anos','Média Porcetagem Reivenstida 5 anos',
              'CAGR Lucro 5 anos','Crescimento esperado LPA',
             'Crescimento esperado EBIT',
             'Crescimento EBIT',
             'Crescimento Margem EBIT',
             'Crescimento LPA',
             'Crescimento Receita','Porcentagem Reinvestida']

def layout_tab7():
    return html.Div([

                    html.Br(),
        
                     dbc.Container([  ### análise indicadores
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Análise Indicadores"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_indicadores_valuation",
                                                                options=[{"label": x, "value": x} for x in indicadores],
                                                                multi=True,
                                                                value=['beta',
                                                                    'Média Crescimento Receitas 5 anos'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                    id='dropdown_comparador_valuation',
                                                                    options=[{'label': 'Média Setor','value': 'SETOR'},
                                                                            {'label': 'Média Subsetor', 'value': 'SUBSETOR'},
                                                                            {'label': 'Média Segmento', 'value': 'SEGMENTO'},
                                                                            {'label': 'Média Classificação Capital', 'value': 'Classificação Capitalização'},
                                                                            {'label': 'Média Brasil', 'value': 'mercado'},
                                                                        ],
                                                                multi=True,
                                                                value=['SEGMENTO'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12}
                                                                    ),
                                                                ],width={'size':8, 'offset': 0},
                                                            ),
                                                    ]),
                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(
                                                                    id="indicadores_valuation_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                    html.Br(),



                                                ]),
                                            ],color="light"),
                                    ]),
                                ]),


                                     

                        ]),
                        
    ])



def valuation_indicadores(dff,indicadores,comparadores):

    try:
        dff = dff.query("LABEL == 'TTM'")
        try:
            empresa = dff['CODIGO'].unique()[0]
        except:
            empresa= '-'

        df_indicadores = dff[indicadores].T
        df_indicadores.rename({df_indicadores.columns[0]: 'Empresa: %s'%empresa},inplace=True, axis=1)

        medias = Medias()
        for comparador in comparadores:
            try:
                if comparador in ['SETOR','SEGMENTO','SUBSETOR']:
                    comp = dff[comparador].unique()[0]
                    value = getattr(medias,comparador.lower())  
                    add1 = value.loc[comp,indicadores].to_frame(name='%s: %s'%(comparador,comp))
                    df_indicadores = df_indicadores.join(add1)
                elif comparador == 'mercado':
                    value = getattr(medias,comparador.lower())
                    value = value.loc[indicadores]
                    df_indicadores = df_indicadores.join(value)
                elif comparador == 'Classificação Capitalização':
                    comp = dff[comparador].unique()[0]
                    value = getattr(medias,'capital')
                    add1 = value.loc[comp,indicadores].to_frame(name='CAPITAL: %s'%(comp))
                    df_indicadores = df_indicadores.join(add1)
            except:
                continue
        
        
        non_percemt =['beta','IC ratio']
        if any(item in non_percemt for item in indicadores):
            df_indicadores.loc[list(set(non_percemt).intersection(indicadores))] = df_indicadores.loc[list(set(non_percemt).intersection(indicadores))].round(decimals=2).astype(str)
            



        df_indicadores.reset_index(inplace=True)
        df_indicadores.rename({'index':''},inplace=True,axis=1)
        
        

        columns=[{"name": i, "id": i, 'type': 'numeric',
                    'format': Format(precision=2, scheme=Scheme.percentage)} for i in df_indicadores.columns]

        columns[0]['editable'] = True

        df_indicadores['id'] = df_indicadores['']
        return  dash_table.DataTable(id='final-table-valuation',fixed_columns={'headers': True,'data': 1},
                                columns=columns,
                                data=df_indicadores.to_dict('records'),
                                row_selectable="single",
                                selected_row_ids=['beta'],
                                persistence=True,
                                persistence_type='session', 
                                style_table={'minWidth': '100%','marginLeft': 'auto', 
                                            'marginRight': 'auto'},
                                
                                style_cell={'font-family':'sans-serif',
                                            'fontSize':12,'height':'auto','whiteSpace': 'normal','width': '200px'
                                        },
                                
                                style_cell_conditional=[{
                                                        'if': {'column_id': ''},
                                                        'textAlign':'left',
                                                        'backgroundColor': colors['first_column'],
                                                        'fontWeight': 'bold'},
                                                        {'if': {'column_id': 'Empresa: %s'%empresa},
                                                                'backgroundColor': colors['column_ttm'],
                                                                'width': '120px','height':'auto'}
                                                    ],

                                style_header={
                                            'backgroundColor': colors['head_table'],
                                            'fontWeight': 'bold','textAlign': 'center','whiteSpace': 'normal',
                                            'height':'50px'
                                        },

                                style_as_list_view=True,
                                export_format='xlsx',
                                export_headers='display',
                                merge_duplicate_headers=True,
                                )

    except:
        return 'Não disponível'