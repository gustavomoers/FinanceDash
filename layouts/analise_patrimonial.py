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
    setor = pd.read_csv(DATA_PATH.joinpath('medias_setor.csv'),low_memory=False,index_col=[0])
    subsetor = pd.read_csv(DATA_PATH.joinpath('medias_subsetor.csv'),low_memory=False,index_col=[0])
    segmento = pd.read_csv(DATA_PATH.joinpath('medias_segmento.csv'),low_memory=False,index_col=[0])
    mercado = pd.read_csv(DATA_PATH.joinpath('medias_mercado_ttm.csv'),low_memory=False,index_col=[0])
    capital = pd.read_csv(DATA_PATH.joinpath('medias_capital.csv'),low_memory=False,index_col=[0])


colors = {'header': "rgb(144, 31, 35)",'first_column': 'rgb(190, 195, 218,.2)',
          'column_ttm': 'rgb(248, 181, 0,.3)','head_table':'rgb(190, 195, 218,.5)',
          'receita': 'rgb(144, 31, 35)','custos': 'rgb(61, 174, 254)','bruto' :'rgb(38,38,38)',
          'ebitda':'rgb(133, 204, 254)','ebit':'rgb(98, 112, 167)','lucro':'rgb(248, 181, 0)',
          'contorno':'rgb(8,48,107)'}

indicadores = [
             'D/E',
             'Dívida/Capital_Inv',
             'Patrimônio/Capital_Inv',
             'Dív_Líq/EBIT',
             'Dív_Líq/PL',
             'Endividamento Financeiro',
             'Endividamento Financeiro Curto Prazo',
             'Dív_Líq/ebitda',
             'PL/Ativos','Passivo/Ativo',
             'Líquidez Corrente', 'VPA Atual',
            ]

def layout_tab5(df):
    return html.Div([
                
                     dbc.Container([ ## demonstração resultado
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Demonstração do Balanço Patrimonial"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_bp_table",
                                                                options=[{'label': 'Anual','value': 'anual'},
                                                                            {'label': 'Trimestral', 'value': 'trimestral'},
                                                                           ],
                                                                value='anual',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_bp_table',
                                                                    updatemode = 'mouseup',
                                                                    min=2009,
                                                                    max=int(this_year),
                                                                    value=[2016,int(this_year)],
                                                                    marks={year: str(year) for year in range(2009,int(this_year)+1,2)},
                                                                    step=1,
                                                                    dots=True,
                                                                    pushable=2,
                                                                    included=True,
                                                                    vertical=False,
                                                                    persistence=True,
                                                                    persistence_type='session',
                                                                    tooltip={'always_visible':False,'placement':'bottom'}),
                                                                ],width={'size':8, 'offset': 0},
                                            ),
                                                    ]),
                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(
                                                                    id="bp_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                ]),
                                            ],color="light"),
                                    ]),
                                ]),
                                ]),
                        
                    html.Br(),
                    html.Br(),
                    html.Br(),
        
                     dbc.Container([  ### análise gráfica
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Análise Gráfica do Capital Investido"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_bp_graph',
                                                                    updatemode = 'mouseup',
                                                                    min=2009,
                                                                    max=int(this_year),
                                                                    value=[2016,int(this_year)],
                                                                    marks={year: str(year) for year in range(2009,int(this_year)+1,2)},
                                                                    step=1,
                                                                    dots=True,
                                                                    pushable=2,
                                                                    included=True,
                                                                    vertical=False,
                                                                    persistence=True,
                                                                    persistence_type='session',
                                                                    tooltip={'always_visible':False,'placement':'bottom'}),
                                                                ],width={'size':10, 'offset': 1},
                                            ),
                                                    ]),
                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                    id="loading-1",
                                                                    type="default",
                                                                     children=[dcc.Graph(id="bp_graph")],
                                                            ),
                                                            
                                                            ],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                ]),
                                            ],color="light"),
                                    ]),
                                ]),
                                ]),
                        

                    html.Br(),
                    html.Br(),
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
                                                                id="dropdown_indicadores_bp",
                                                                options=[{"label": x, "value": x} for x in indicadores],
                                                                multi=True,
                                                                value=['D/E',
                                                                     'Dívida/Capital_Inv'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                    id='dropdown_comparador_bp',
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
                                                                    id="indicadores_bp_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_bp_indic',
                                                                    updatemode = 'mouseup',
                                                                    min=2009,
                                                                    max=int(this_year),
                                                                    value=[2016,int(this_year)],
                                                                    marks={year: str(year) for year in range(2009,int(this_year)+1,2)},
                                                                    step=1,
                                                                    dots=True,
                                                                    pushable=2,
                                                                    included=True,
                                                                    vertical=False,
                                                                    persistence=True,
                                                                    persistence_type='session',
                                                                    tooltip={'always_visible':False,'placement':'bottom'}),
                                                                    ],width={'size': 10, 'offset': 1},
                                                            ),

                                                            ]),

                                                    html.Br(),
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(

                                                                    dcc.Loading(
                                                                            id="loading-1",
                                                                            type="default",
                                                                            children=[dcc.Graph(id='bp_indicadores_graph')],
                                                                    ),
                                                                    
                                                                    
                                                                    )],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),


                                                ]),
                                            ],color="light"),
                                    ]),
                                ]),


                                     

                        ]),
                        
    ])



def layout_bp_table(dff,tipo,year):

    

    df1 = dff.loc[(dff['tipo_resultado'] == tipo)]             
            

            
        
    df1 = df1[(df1['ano'] >= year[0]) & (df1['ano'] <= year[1])]
    
 
    bp = df1.sort_values(by='DT_FIM_EXERC')
    bp1 = bp.pivot_table(columns=['ano','LABEL'], values=['Ativo Total',
                                                            'Ativo Circulante',
                                                            'Aplicações Financeiras',
                                                            'Caixa e Equivalentes de Caixa',
                                                            'Ativo Não Circulante',
                                                            'Ativo Realizável a Longo Prazo',
                                                            'Investimentos',
                                                            'Passivo Total',
                                                            'Passivo Circulante',
                                                            'Dívida curto prazo',
                                                            'Passivo Não Circulante',
                                                            'Dívida longo prazo',
                                                            'Patrimônio Líquido Con Final',
                                                            'Participação dos Não Controladores Final'])
    index_order = ['Ativo Total',
                    'Ativo Circulante',
                    'Aplicações Financeiras',
                    'Caixa e Equivalentes de Caixa',
                    'Ativo Não Circulante',
                    'Ativo Realizável a Longo Prazo',
                    'Investimentos',
                    'Passivo Total',
                    'Passivo Circulante',
                    'Dívida curto prazo',
                    'Passivo Não Circulante',
                    'Dívida longo prazo',
                    'Patrimônio Líquido Con Final',
                    'Participação dos Não Controladores Final']


    bp3 = bp1.reindex(index_order)
    bp3.rename({
                'Ativo Circulante': ' Ativo Circulante',
                'Aplicações Financeiras': '  Aplicações Financeiras',
                'Caixa e Equivalentes de Caixa': '  Caixa e Equivalentes de Caixa',
                'Ativo Não Circulante': ' Ativo Não Circulante',
                'Ativo Realizável a Longo Prazo': '  Ativo Realizável a Longo Prazo',
                'Investimentos': '  Investimentos',
                'Passivo Circulante': ' Passivo Circulante',
                'Dívida curto prazo': '  Dívida curto prazo',
                'Passivo Não Circulante': ' Passivo Não Circulante',
                'Dívida longo prazo': '  Dívida longo prazo',
                'Patrimônio Líquido Con Final': ' Patrimônio Líquido Consolidado',
                'Participação dos Não Controladores Final': '  Participação dos Não Controladores'},inplace=True)

    bp3 = bp3[bp3.columns[::-1]]
    bp3.reset_index(inplace=True)
    bp3.columns = bp3.columns.droplevel(0)
    

    try:
        df2 = dff
        df2 = df2.loc[(df2['LABEL'] == 'TTM')]               
            
            
        df2 = df2[(df2['ano'] >= year[0]) & (df2['ano'] <= year[1])]

        df2 = df2.pivot_table(columns=['LABEL'], values=['Ativo Total',
                                                            'Ativo Circulante',
                                                            'Aplicações Financeiras',
                                                            'Caixa e Equivalentes de Caixa',
                                                            'Ativo Não Circulante',
                                                            'Ativo Realizável a Longo Prazo',
                                                            'Investimentos',
                                                            'Passivo Total',
                                                            'Passivo Circulante',
                                                            'Dívida curto prazo',
                                                            'Passivo Não Circulante',
                                                            'Dívida longo prazo',
                                                            'Patrimônio Líquido Con Final',
                                                            'Participação dos Não Controladores Final'])

        index_order = ['Ativo Total',
                            'Ativo Circulante',
                            'Aplicações Financeiras',
                            'Caixa e Equivalentes de Caixa',
                            'Ativo Não Circulante',
                            'Ativo Realizável a Longo Prazo',
                            'Investimentos',
                            'Passivo Total',
                            'Passivo Circulante',
                            'Dívida curto prazo',
                            'Passivo Não Circulante',
                            'Dívida longo prazo',
                            'Patrimônio Líquido Con Final',
                            'Participação dos Não Controladores Final']

        df2 = df2.reindex(index_order)

        df2.rename({
                'Ativo Circulante': ' Ativo Circulante',
                'Aplicações Financeiras': '  Aplicações Financeiras',
                'Caixa e Equivalentes de Caixa': '  Caixa e Equivalentes de Caixa',
                'Ativo Não Circulante': ' Ativo Não Circulante',
                'Ativo Realizável a Longo Prazo': '  Ativo Realizável a Longo Prazo',
                'Investimentos': '  Investimentos',
                'Passivo Circulante': ' Passivo Circulante',
                'Dívida curto prazo': '  Dívida curto prazo',
                'Passivo Não Circulante': ' Passivo Não Circulante',
                'Dívida longo prazo': '  Dívida longo prazo',
                'Patrimônio Líquido Con Final': ' Patrimônio Líquido Consolidado',
                'Participação dos Não Controladores Final': '  Participação dos Não Controladores'},inplace=True)

        df2.reset_index(inplace=True)

        bp3.insert(1,'Último',df2['TTM'])
    except:
        bp3 = bp3


    


    ahs = []
    for x in range(1,(len(bp3.columns)-1)):
        data = (bp3[bp3.columns[x]]-bp3[bp3.columns[x+1]])/np.abs(bp3[bp3.columns[x+1]])
        ahs.append(data)

    y = 0
    for x in range(2,(len(bp3.columns)+len(ahs)-1),2):

        bp3.insert(x,'AH_%i'%y,ahs[y])
        y=y+1

    columns = [{'name': '', 'id': '', 'type': 'text', 'editable': True}]
    formatation = []
    for x in range(1,(len(bp3.columns))):
        if (x % 2) == 0:
            columns.append({"name": 'AH %', "id": bp3.columns[x],'type':'numeric',
                  'format': Format(precision=2, scheme=Scheme.percentage),
                            'hideable': True})
            formatation.append(bp3.columns[x])

        else:
            columns.append({"name": bp3.columns[x], "id": bp3.columns[x],'type':'numeric',
                  'format': Format(precision=2,group=',',group_delimiter='.',
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                    si_prefix=Prefix.mega, symbol_suffix=' ')})
    
   
    for x in range(len(columns)):
        if columns[x]['id'] == 'Último':
             columns[x]['hideable'] = True
                
    
    
    red_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} < 0'.format(x)},
        'color': 'red'}  for x in formatation]
    
    green_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 0'.format(x)},
        'color': 'green'}  for x in formatation]

    red_values.extend(green_values)

    return ([dash_table.DataTable(
                            id="final-table-bp",  fixed_columns={'headers': True,'data': 1},
                            columns=columns,
                            data=bp3.to_dict('records'),   
                            style_table={'minWidth': '100%','marginLeft': 'auto', 
                                         'marginRight': 'auto'},
                            style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto'},
                            style_cell={
                                        'height': 'auto',
                                        # all three widths are needed
                                        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                        'whiteSpace': 'normal','font-family':'sans-serif',
                                        'fontSize':12,
                                    },
        
                            style_cell_conditional=[{
                                                    'if': {'column_editable': True},
                                                    'width': '180px','textAlign':'left',
                                                    'backgroundColor': colors['first_column'],
                                                    'fontWeight': 'bold'},
                                                    {'if': {'column_id': 'Último'},
                                                            'backgroundColor': colors['column_ttm']}
                                                ],

                            style_data_conditional=red_values,

                            style_header={
                                        'backgroundColor': colors['head_table'],
                                        'fontWeight': 'bold','textAlign': 'center'
                                    },

                            style_as_list_view=True,
                            export_format='xlsx',
                            export_headers='display',
                            merge_duplicate_headers=True,
                            )])



def bp_graph(dff,year):

    dff[['Patrimônio Líquido Con Final']] = dff[['Patrimônio Líquido Con Final']].fillna(value=0)
    dff[['Patrimônio/Capital_Inv']] = dff[['Patrimônio/Capital_Inv']].fillna(value=0)
    dff[['Dívida/Capital_Inv']] = dff[['Dívida/Capital_Inv']].fillna(value=0)
    dff[['Margem EBIT']] = dff[['Margem EBIT']].fillna(value=0)
    dff[['Margem líquida']] = dff[['Margem líquida']].fillna(value=0)

        
    dff = dff.loc[(dff['tipo_resultado'] == 'anual') | (dff['LABEL'] == 'TTM')]             
        
    dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])] 

    fig = go.Figure()

    fig.add_bar(name = 'Patrimônio Líquido',y=dff['Patrimônio Líquido Con Final'],x=dff['DT_FIM_EXERC'],marker_color=colors['receita'], xperiod="M12",
                    customdata=dff[['LABEL','Patrimônio/Capital_Inv']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Patrimônio Líquido</b>: R%{y:$,.0}<br>"+
                    "<b>Patrimônio/Capital_Inv</b>: %{customdata[1]:.2%}")

    fig.add_bar(name = 'Dívida Bruta',y=dff['Dívida Bruta'],x=dff['DT_FIM_EXERC'],marker_color=colors['custos'], xperiod="M12",
                    customdata=dff[['LABEL','Dívida/Capital_Inv']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Dívida Bruta</b>: R%{y:$,.0}<br>"+
                    "<b>Dívida/Capital_Inv</b>: %{customdata[1]:.2%}")

    fig.add_bar(name='Disponibilidade',y=dff['Disponibilidade'],x=dff['DT_FIM_EXERC'],marker_color=colors['bruto'], xperiod="M12",
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Disponibilidade</b>: R%{y:$,.0}<br>")

    fig.add_scatter(name='Capital Investido',y=dff['Capital Investido'],x=dff['DT_FIM_EXERC'],marker_color=colors['lucro'], xperiod="M12",
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Capital Investido</b>: R%{y:$,.0}<br>")


    fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
    fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
    fig.update_layout(title_text='Capital Investido',template='seaborn',
                         barmode='group')  


    return fig



def bp_indicadores(dff,indicadores,comparadores):

    try:
        dff = dff.query("LABEL == 'TTM'")
        try:
            empresa = dff['CODIGO'].unique()[0]
        except:
            empresa= '-'
        

        non_percemt = ['Dív_Líq/EBIT',
             'Dív_Líq/PL',
             'Dív_Líq/ebitda',
             'PL/Ativos','Passivo/Ativo',
             'Líquidez Corrente', 'VPA Atual']

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
        
        

        if any(item in non_percemt for item in indicadores):
            df_indicadores.loc[list(set(non_percemt).intersection(indicadores))] = df_indicadores.loc[list(set(non_percemt).intersection(indicadores))].round(decimals=2).astype(str)
                

        df_indicadores.reset_index(inplace=True)
        df_indicadores.rename({'index':''},inplace=True,axis=1)
        
        

        columns=[{"name": i, "id": i, 'type': 'numeric',
                    'format': Format(precision=2, scheme=Scheme.percentage)} for i in df_indicadores.columns]

        columns[0]['editable'] = True

        df_indicadores['id'] = df_indicadores['']
        return  dash_table.DataTable(
                                id="final-table-bp",  fixed_columns={'headers': True,'data': 1},
                                columns=columns,
                                data=df_indicadores.to_dict('records'),
                                row_selectable="single",
                                selected_row_ids=['D/E'],
                                persistence=True,
                                persistence_type='session', 
                                style_table={'minWidth': '100%','marginLeft': 'auto', 
                                            'marginRight': 'auto'},
                                
                                style_cell={'font-family':'sans-serif',
                                            'fontSize':12,'height':'auto','whiteSpace': 'normal','width': '200px'
                                        },
                                
                                style_cell_conditional=[{
                                                        'if': {'column_editable': True},
                                                        'textAlign':'left',
                                                        'backgroundColor': colors['first_column'],
                                                        'fontWeight': 'bold'},
                                                        {'if': {'column_id': 'Empresa: %s'%empresa},
                                                                'backgroundColor': colors['column_ttm'],
                                                                'width': '120px','height':'auto'}
                                                    ],

                                style_header={
                                            'backgroundColor': colors['head_table'],
                                            'fontWeight': 'bold','textAlign': 'center','height':'50px',
                                            'whiteSpace': 'normal',
                                        },

                                style_as_list_view=True,
                                export_format='xlsx',
                                export_headers='display',
                                merge_duplicate_headers=True,
                                )

    except:
        return 'Não disponível'



def bp_indicadores_graph(slctd_row_indices,company,year):

    try:
        indic = slctd_row_indices[0]

    except:
        indic = 'D/E'


    d1 = pd.DataFrame.from_dict(company) 
    d1= d1[(d1['tipo_resultado'] == 'anual') | (d1['LABEL'] == 'TTM') ] 
     

    try:
        d1['VPA Atual'] = np.nan_to_num(d1['VPA histórico']) + np.nan_to_num(d1['VPA Atual'])
    except:
        d1=d1

    d1 = d1[(d1['ano'] >= year[0]) & (d1['ano'] <= year[1])]
    fig = go.Figure()

    fig.add_bar(showlegend=True,name=indic,y=d1[indic],x=d1['DT_FIM_EXERC'],
                            marker_color=colors['receita'], xperiod="M12",text = d1[indic])
            
        
    if not indic in ['Dív_Líq/EBIT','Dív_Líq/PL','Dív_Líq/ebitda','PL/Ativos','Passivo/Ativo','Líquidez Corrente', 'VPA Atual']:
        fig.update_yaxes(tickformat=".2%")

        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],marker_line_width=1.5, opacity=0.8,
                            texttemplate='%{text:.1%}', textposition='inside')
        fig.update_layout(template='seaborn',barmode='relative',uniformtext_minsize=8,uniformtext_mode='hide')
        
    else:
        fig.update_yaxes(tickformat=".2f")

        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],marker_line_width=1.5, opacity=0.8,
                            texttemplate='%{text:.1f}', textposition='inside')
        fig.update_layout(template='seaborn',barmode='relative',uniformtext_minsize=8,uniformtext_mode='hide',
                            yaxis = dict(fixedrange = False))

    return fig
    