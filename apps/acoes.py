import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from pandas.core.indexes import multi
import dash_table
from dash_table.Format import Format, Group, Prefix, Scheme, Symbol
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import re
import locale
import pathlib
from app import app
from layouts import summary, analise_operacional,analise_caixa,analise_patrimonial

locale.setlocale(locale.LC_ALL, '')

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../DADOS").resolve()

df = pd.read_csv(DATA_PATH.joinpath('df_princial_preco_atualizado.csv'),low_memory=False)  # GregorySmith Kaggle
df['DT_FIM_EXERC'] = pd.to_datetime(df['DT_FIM_EXERC'])
df['drop_options'] = df['CODIGO']+ ': ' + df['NAME_PREG']
df = df.replace(np.inf, np.nan)
df= df[df['ano'].notnull()]
df['ano'] = df['ano'].astype(int)
label = df['drop_options'].unique()
value = df['CODIGO'].unique()




layout = html.Div([

    dcc.Store(id='memory-output'),
    

   
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Container([  ## container select company and summary
                dbc.Row([
                        dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader(
                                        dcc.Dropdown(
                                                    id="dropdown_company",
                                                    options=[{"label": x, "value": y} for x,y in list(zip(label,value))],
                                                    clearable=False,
                                                    placeholder="Selecione uma Empresa",
                                                    style={'font-family':'sans-serif',
                                                                    'fontSize':12})),
                                        dbc.CardBody([
       
                                                        dbc.Row([
                                                            dbc.Col([
                                                                    dbc.CardImg(id='company-logo'
                                                                    ),
                                                        
                                                                ],width={'size': 2, 'offset': 0},
                                                                align='center'),
                                                            dbc.Col([
                                                                html.Div(id='name-link')          
                                                                
                                                                ],width={'size': 4, 'offset': 1},
                                                                align='center'), 
                                                            dbc.Col([
                                                                
                                                                    html.P(id='descr',
                                                                            ),       
                                                                ],width={'size': 4, 'offset': 1},
                                                                align='center'), 
                                                    ]),
                                                html.Br(),
                                                dbc.Row([
                                                        dbc.Col([
                                                             html.Div(id='first-summary-table') 
                                                            ],width={'size': 6, 'offset': 0},
                                                                align='center'),
                                                            
                                                        dbc.Col([
                                                             html.Div(id='second-summary-table') 
                                                            ],width={'size':6, 'offset': 0},
                                                                align='center'),
                                                        
                                                        ]),
                                                ]),
                                ]),
                        ]),
                    ]),
                ]),
                   

    
    html.Br(),
    html.Br(),
    html.Br(),
    

    dbc.Row([dbc.Col(html.Div([  ## tabs
        html.Div([
            dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-1', children = [
                dcc.Tab(label = 'Resumo', value = 'tab-1',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Preço', value = 'tab-2',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Operações', value = 'tab-3',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Caixa', value = 'tab-4',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Patrimônio', value = 'tab-5',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Dividendos', value = 'tab-6',className='custom-tab',
                        selected_className='custom-tab--selected'),
                dcc.Tab(label = 'Valuation', value = 'tab-7',className='custom-tab',
                        selected_className='custom-tab--selected'),
            ], parent_className='custom-tabs',
                className='custom-tabs-container'),
               html.Br(),
                html.Br(),
                html.Br(),
            html.Div(id = 'tabs-content-inline')
        ] ),
        ]),width={'size': 10, 'offset': 1}
                    )])
])


# callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# callback for store chosen company data 
@app.callback(Output('memory-output', 'data'),
              Input('dropdown_company', 'value'))
def filter_company(company):

    df1 = df.loc[(df['CODIGO'] == company)]

    if df1['GRUPO_DFP'].nunique() == 2:
        df1 = df1[df1['GRUPO_DFP'] != 'DF_IND'] 

    return df1.to_dict('records')    


# callback for company summary
@app.callback(Output('company-logo', 'src'),Output('name-link', 'children'),
              Output('first-summary-table', 'children'), Output('second-summary-table', 'children'),
              Output('descr','children'),
              Input('memory-output', 'data'))
def update_summary(value):
    dff = pd.DataFrame.from_dict(value)

    output = dff['CDO_STRIP'].unique()[0]
    nome_empresarial = dff['Nome_Empresarial'].unique()[0]
    codigos = dff['CODIGOS'].unique()[0]
    setor = dff['SETOR'].unique()[0]
    subsetor = dff['SUBSETOR'].unique()[0]
    segmento = dff['SEGMENTO'].unique()[0]
    world = dff['DAMODARAN_GROUP'].unique()[0]
    descr = dff['Descricao_Atividade'].unique()[0]
    cnpj = dff['CNPJ_Companhia'].unique()[0]
    pagina_web = dff['Pagina_Web'].unique()[0]
    seg_b3 = dff['SEGMENTO_B3'].unique()[0]
    class_capital = dff['Classificação Capitalização'].unique()[0]
    
    

    try:
        dff = dff.loc[(dff['LABEL'] == 'TTM')]
        dff['current_price'].replace(np.nan,0,inplace=True)
        dff['Valor de Mercado Atual'].replace(np.nan,0,inplace=True)
        dff['Qtde Total de Ações'].replace(np.nan,0,inplace=True)
        dff['Qtde Ações Ordinárias'].replace(np.nan,0,inplace=True)
        dff['Qtde Ações Preferenciais'].replace(np.nan,0,inplace=True)

        price = dff['current_price'].unique()[0]
        mv_value = dff['Valor de Mercado Atual'].unique()[0]
        total_papeis = dff['Qtde Total de Ações'].unique()[0]
        total_on = dff['Qtde Ações Ordinárias'].unique()[0]
        total_pn = dff['Qtde Ações Preferenciais'].unique()[0]
        class_capital = dff['Classificação Capitalização'].unique()[0]
    except:
        price = 0
        mv_value = 0
        total_papeis = 0
        total_on = 0
        total_pn = 0
        class_capital = '-'



    return (app.get_asset_url("%s.svg"%output), summary.summary_name(nome_empresarial,cnpj,pagina_web),
            summary.summary_table_first(codigos,seg_b3,price,total_papeis,total_on,total_pn,mv_value),
            summary.summary_table_setor(setor,subsetor,segmento,class_capital,world),
            descr)


# callback for update content on tabs
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'),Input('memory-output', 'data'))
def render_content(tab,data):

    dff = pd.DataFrame.from_dict(data)

    if tab == 'tab-1':
        return html.Div([
            html.H3('Display content here in tab 2', style = {'text-align': 'center', 'margin-top': '100px', 'color':'black'})
        ])


    elif tab == 'tab-2':
        return html.Div([
            html.H3('Display content here in tab 2', style = {'text-align': 'center', 'margin-top': '100px', 'color':'black'})
        ])


    elif tab == 'tab-3':
        return analise_operacional.layout_tab3(dff)


    elif tab == 'tab-4':
        return analise_caixa.layout_tab4(dff)


    elif tab == 'tab-5':
        return analise_patrimonial.layout_tab5(dff)


    elif tab == 'tab-6':
        return html.Div([
            html.H3('Display content here in tab 4', style = {'text-align': 'center', 'margin-top': '100px', 'color':'black'})
        ])

    
    elif tab == 'tab-7':
        return html.Div([
            html.H3('Display content here in tab 4', style = {'text-align': 'center', 'margin-top': '100px', 'color':'black'})
        ])


# callback for dre table
@app.callback(Output("dre_table", "children"),
    Input("memory-output", "data"),Input("dropdown_dre_table", "value"),
    Input("slider_dre_table", "value"))
def update_dre_table(company,tipo,year):

    dff = pd.DataFrame.from_dict(company)
  
    return analise_operacional.layout_dre_table(dff,tipo,year)


# callback for dre graph
@app.callback(Output("dre_graph", "figure"),
    Input("memory-output", "data"),Input("dropdown_dre_graph", "value"),
    Input("slider_dre_graph", "value"))
def update_dre_graph(company,tipo,year):
   
    dff = pd.DataFrame.from_dict(company)
    
    return analise_operacional.dre_graph(dff,tipo,year)


# callback for dre indicadores table
@app.callback(Output("indicadores_dre_table", "children"),
    Input("memory-output", "data"),Input("dropdown_indicadores_dre", "value"),
    Input("dropdown_comparador_dre", "value"))
def update_dre_indicadores(company,indicadores,comparadores):

    dff = pd.DataFrame.from_dict(company)

    return analise_operacional.dre_indicadores(dff,indicadores,comparadores) 


# callback for dre indicadores graph
@app.callback(Output(component_id='dre_indicadores_graph', component_property='figure'),
     Input(component_id='final-table-1', component_property='derived_virtual_selected_row_ids'),
     Input("memory-output", "data"),Input("slider_dre_indic", "value"))
def update_dre_indicadores_graph(slctd_row_indices,company,year):
    if slctd_row_indices is None:
        slctd_row_indices = []
    return analise_operacional.dre_indicadores_graph(slctd_row_indices,company,year)


# callback for dfc table
@app.callback(Output("dfc_table", "children"),
    Input("memory-output", "data"),Input("slider_dfc_table", "value"))
def update_dfc_table(company,year):

    dff = pd.DataFrame.from_dict(company)
  
    return analise_caixa.layout_dfc_table(dff,year)


# callback for dfc graph
@app.callback(Output("dfc_graph", "figure"),
    Input("memory-output", "data"),Input("dropdown_dfc_graph", "value"),
    Input("slider_dfc_graph", "value"))
def update_dfc_graph(company,tipo,year):
   
    dff = pd.DataFrame.from_dict(company)
    
    return analise_caixa.dfc_graph(dff,tipo,year)


# callback for dfc indicadores table
@app.callback(Output("indicadores_dfc_table", "children"),
    Input("memory-output", "data"),Input("dropdown_indicadores_dfc", "value"),
    Input("dropdown_comparador_dfc", "value"))
def update_dfc_indicadores(company,indicadores,comparadores):

    dff = pd.DataFrame.from_dict(company)

    return analise_caixa.dfc_indicadores(dff,indicadores,comparadores) 


# callback for dfc indicadores graph
@app.callback(Output(component_id='dfc_indicadores_graph', component_property='figure'),
     Input(component_id='final-table-dfc', component_property='derived_virtual_selected_row_ids'),
     Input("memory-output", "data"),Input("slider_dfc_indic", "value"))
def update_dfc_indicadores_graph(slctd_row_indices,company,year):
    if slctd_row_indices is None:
        slctd_row_indices = []
    return analise_caixa.dfc_indicadores_graph(slctd_row_indices,company,year)


# callback for bp table
@app.callback(Output("bp_table", "children"),
    Input("memory-output", "data"),Input("dropdown_bp_table", "value"),
    Input("slider_bp_table", "value"))
def update_bp_table(company,tipo,year):

    dff = pd.DataFrame.from_dict(company)
  
    return analise_patrimonial.layout_bp_table(dff,tipo,year)


# callback for bp graph
@app.callback(Output("bp_graph", "figure"),
    Input("memory-output", "data"),
    Input("slider_bp_graph", "value"))
def update_bp_graph(company,year):
   
    dff = pd.DataFrame.from_dict(company)
    
    return analise_patrimonial.bp_graph(dff,year)


# callback for bp indicadores table
@app.callback(Output("indicadores_bp_table", "children"),
    Input("memory-output", "data"),Input("dropdown_indicadores_bp", "value"),
    Input("dropdown_comparador_bp", "value"))
def update_bp_indicadores(company,indicadores,comparadores):

    dff = pd.DataFrame.from_dict(company)

    return analise_patrimonial.bp_indicadores(dff,indicadores,comparadores) 


# callback for bp indicadores graph
@app.callback(Output(component_id='bp_indicadores_graph', component_property='figure'),
     Input(component_id='final-table-bp', component_property='derived_virtual_selected_row_ids'),
     Input("memory-output", "data"),Input("slider_bp_indic", "value"))
def update_bp_indicadores_graph(slctd_row_indices,company,year):
    if slctd_row_indices is None:
        slctd_row_indices = []
    return analise_patrimonial.bp_indicadores_graph(slctd_row_indices,company,year)




