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

indicadores = ['Margem bruta','Margem EBITDA',
             'Margem EBIT',
             'Margem líquida',
             'Taxa efetiva de imposto',
             'ROE',
             'Porcentagem Retida',
             'ROA',
             'ROIC',
             'Giro dos Ativos',
             'Crescimento esperado LPA',
             'Crescimento esperado EBIT',
             'Crescimento Receita',
             'LPA Atual',]

def layout_tab3():
    return html.Div([
                
                     dbc.Container([ ## demonstração resultado
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Demonstração do Resultado do Exercício"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_dre_table",
                                                                options=[{'label': 'Anual','value': 'anual'},
                                                                            {'label': 'Trimestral', 'value': 'trimestral'},
                                                                            {'label': 'Anualizado', 'value': 'anualizado'},
                                                                            {'label': '1º Trimestre', 'value': '1 trim'},
                                                                            {'label': '2º Trimestre', 'value': '2 trim'},
                                                                            {'label': '3º Trimestre', 'value': '3 trim'},
                                                                            {'label': '4º Trimestre', 'value': '4 trim'},],
                                                                value='anual',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dre_table',
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
                                                                    id="dre_table")],
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
                                                dbc.CardHeader("Análise Gráfica Resultado do Exercício"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_dre_graph",
                                                                options=[{'label': 'Anual','value': 'anual'},
                                                                            {'label': 'Trimestral', 'value': 'trimestral'},
                                                                            {'label': 'Anualizado', 'value': 'anualizado'},
                                                                            {'label': 'Receitas Stack', 'value': 'receita stack'},
                                                                        
                                                                        ],
                                                                value='anual',
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dre_graph',
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

                                                            dcc.Loading(
                                                                    id="loading-1",
                                                                    type="default",
                                                                    children=[dcc.Graph(id="dre_graph")]
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
                                                                id="dropdown_indicadores_dre",
                                                                options=[{"label": x, "value": x} for x in indicadores],
                                                                multi=True,
                                                                value=['Margem bruta','Margem EBIT','Margem líquida',
                                                                'ROE','ROIC'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                    id='dropdown_comparador_dre',
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
                                                                    id="indicadores_dre_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dre_indic',
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
                                                                            children=[dcc.Graph(id='dre_indicadores_graph')]
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



def layout_dre_table(dff,tipo,year):

    if tipo in ['1 trim','2 trim','3 trim','4 trim']:

        df1 = dff.loc[(dff['trimestre'] == tipo)]             
    

    elif tipo == 'anualizado':

        df1 = dff.loc[(dff['tipo_resultado'] == 'trimestral')]             
      
    else:

        df1 = dff.loc[(dff['tipo_resultado'] == tipo)]             
      
            
        
    df1 = df1[(df1['ano'] >= year[0]) & (df1['ano'] <= year[1])]
    
    if tipo == 'anualizado':
        df1.sort_values('DT_FIM_EXERC', inplace=True)

        lista_anu = ['Custos','Resultado Bruto','Despesas/Receitas Operacionais','EBITDA',
                           'Depreciação, Amortização e Exaustão','EBIT','Resultado Financeiro',
                          'Imposto','Lucro Líquido',
                           'Lucro Atribuído a não controladores','Lucro Atribuído a Controladores']

        anualizado = df1['Receita Líquida'].rolling(min_periods=4,window=4).sum()[::-4].to_frame()
        for item in lista_anu:
            anualizado = anualizado.join(df1[item].rolling(min_periods=4,window=4).sum()[::-4])

        anualizado.dropna(how='all',inplace=True)

        anualizado.reset_index(inplace=True)

        anualizado.drop('index',axis=1,inplace=True)

        labels = df1['LABEL'][::-1].to_list()

        lista12 = []
        for x in range(0,len(anualizado)*4,4):
            lista12.append(labels[x+3]+' - '+labels[x])

        labels_anu = pd.DataFrame(lista12)

        anualizado = anualizado.join(labels_anu)

        anualizado= anualizado.melt(id_vars=[0],var_name='conta',value_name='VL_CONTA')

        anualizado = anualizado.pivot_table(columns=0,index='conta',values='VL_CONTA')

        index_order = ['Receita Líquida','Custos','Resultado Bruto','Despesas/Receitas Operacionais','EBITDA',
                           'Depreciação, Amortização e Exaustão','EBIT','Resultado Financeiro',
                          'Imposto','Lucro Líquido',
                           'Lucro Atribuído a não controladores','Lucro Atribuído a Controladores']
        anualizado = anualizado.reindex(index_order)

        anualizado = anualizado[anualizado.columns[::-1]]
        anualizado.reset_index(inplace=True)

        anualizado = anualizado.rename({'conta': ''},axis=1)
        rev3 = anualizado
    
    
    
    else:
        rev = df1.sort_values(by='DT_FIM_EXERC')
        rev1 = rev.pivot_table(columns=['ano','LABEL'], values=['Receita Líquida', 'Custos', 'Resultado Bruto',
                                                        'Despesas/Receitas Operacionais',
                                                        'Depreciação, Amortização e Exaustão',
                                                        'EBIT',
                                                        'Resultado Financeiro',
                                                        'Imposto',
                                                        'Lucro Líquido',
                                                        'Lucro Atribuído a não controladores',
                                                         'Lucro Atribuído a Controladores' ,
                                                          'EBITDA'])
        index_order = ['Receita Líquida','Custos','Resultado Bruto','Despesas/Receitas Operacionais','EBITDA',
                       'Depreciação, Amortização e Exaustão','EBIT','Resultado Financeiro',
                      'Imposto','Lucro Líquido',
                       'Lucro Atribuído a não controladores','Lucro Atribuído a Controladores']
        rev3 = rev1.reindex(index_order)

        rev3 = rev3[rev3.columns[::-1]]
        rev3.reset_index(inplace=True)
        rev3.columns = rev3.columns.droplevel(0)
    

    try:
        if tipo == 'anual':
            df2 = dff
            df2 = df2.loc[(df2['LABEL'] == 'TTM')]               
            
            
            df2 = df2[(df2['ano'] >= year[0]) & (df2['ano'] <= year[1])]

            df2 = df2.pivot_table(columns=['LABEL'], values=['Receita Líquida', 'Custos', 'Resultado Bruto',
                                                                'Despesas/Receitas Operacionais',
                                                                'Depreciação, Amortização e Exaustão',
                                                                'EBIT',
                                                                'Resultado Financeiro',
                                                                'Imposto',
                                                                'Lucro Líquido',
                                                                'Lucro Atribuído a não controladores',
                                                                'Lucro Atribuído a Controladores' ,
                                                                'EBITDA'])
            index_order = ['Receita Líquida','Custos','Resultado Bruto','Despesas/Receitas Operacionais','EBITDA',
                            'Depreciação, Amortização e Exaustão','EBIT','Resultado Financeiro',
                            'Imposto','Lucro Líquido',
                            'Lucro Atribuído a não controladores','Lucro Atribuído a Controladores']
            df2 = df2.reindex(index_order)

            df2.reset_index(inplace=True)

            rev3.insert(1,'TTM',df2['TTM'])
    except:
        rev3 = rev3




    ahs = []
    for x in range(1,(len(rev3.columns)-1)):
        data = (rev3[rev3.columns[x]]-rev3[rev3.columns[x+1]])/np.abs(rev3[rev3.columns[x+1]])
        ahs.append(data)

    y = 0
    for x in range(2,(len(rev3.columns)+len(ahs)-1),2):

        rev3.insert(x,'AH_%i'%y,ahs[y])
        y=y+1

    columns = [{'name': '', 'id': '', 'type': 'text', 'editable': True}]
    formatation = []
    for x in range(1,(len(rev3.columns))):
        if (x % 2) == 0:
            columns.append({"name": 'AH %', "id": rev3.columns[x],'type':'numeric',
                  'format': Format(precision=2, scheme=Scheme.percentage),
                            'hideable': True})
            formatation.append(rev3.columns[x])

        else:
            columns.append({"name": rev3.columns[x], "id": rev3.columns[x],'type':'numeric',
                  'format': Format(precision=2,group=',',group_delimiter='.',
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                    si_prefix=Prefix.mega, symbol_suffix=' ')})
    
    if tipo == 'anual':
        for x in range(len(columns)):
            if columns[x]['id'] == 'TTM':
                columns[x]['hideable'] = True
                
    
    
    red_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} < 0'.format(x)},
        'color': 'red'}  for x in formatation]
    
    green_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 0'.format(x)},
        'color': 'green'}  for x in formatation]

    red_values.extend(green_values)

    return ([dash_table.DataTable(
                            id="final-table",  fixed_columns={'headers': True,'data': 1},
                            columns=columns,
                            data=rev3.to_dict('records'),   
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
                                                    {'if': {'column_id': 'TTM'},
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



def dre_graph(dff,tipo,year):

    dff[['Crescimento Receita']] = dff[['Crescimento Receita']].fillna(value=0)
    dff[['Margem bruta']] = dff[['Margem bruta']].fillna(value=0)
    dff[['Margem EBITDA']] = dff[['Margem EBITDA']].fillna(value=0)
    dff[['Margem EBIT']] = dff[['Margem EBIT']].fillna(value=0)
    dff[['Margem líquida']] = dff[['Margem líquida']].fillna(value=0)

    if tipo == 'anualizado':

        dff = dff.loc[(dff['tipo_resultado'] == 'trimestral')]             
        
        dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])] 
 
        dff.sort_values('DT_FIM_EXERC', inplace=True)

        lista_anu = ['Custos','Resultado Bruto','Despesas/Receitas Operacionais','EBITDA',
                           'Depreciação, Amortização e Exaustão','EBIT','Resultado Financeiro',
                          'Imposto','Lucro Líquido',
                           'Lucro Atribuído a não controladores','Lucro Atribuído a Controladores']

        anualizado = dff['Receita Líquida'].rolling(min_periods=4,window=4).sum()[::-4].to_frame()
        for item in lista_anu:
            anualizado = anualizado.join(dff[item].rolling(min_periods=4,window=4).sum()[::-4])
            
        
        anualizado.dropna(how='all',inplace=True)

        anualizado.reset_index(inplace=True)

        anualizado.drop('index',axis=1,inplace=True)
        anualizado = anualizado[::-1]
        
        labels = dff['LABEL'][::-1].to_list()

        lista12 = []
        for x in range(0,len(anualizado)*4,4):
            lista12.append(labels[x+3]+' - '+labels[x])

        labels_anu = pd.DataFrame(lista12)

        anualizado = anualizado.join(labels_anu)



        anualizado['Crescimento Receita'] = anualizado['Receita Líquida'].pct_change()

        anualizado['Margem bruta'] = anualizado['Resultado Bruto']/anualizado['Receita Líquida']
        anualizado['Margem EBITDA'] = anualizado['EBITDA']/anualizado['Receita Líquida']
        anualizado['Margem EBIT'] = anualizado['EBIT']/anualizado['Receita Líquida']
        anualizado['Margem líquida'] = anualizado['Lucro Atribuído a Controladores']/anualizado['Receita Líquida']

        anualizado[['Crescimento Receita']] = anualizado[['Crescimento Receita']].fillna(value=0)
        anualizado[['Margem bruta']] = anualizado[['Margem bruta']].fillna(value=0)
        anualizado[['Margem EBITDA']] = anualizado[['Margem EBITDA']].fillna(value=0)
        anualizado[['Margem EBIT']] = anualizado[['Margem EBIT']].fillna(value=0)
        anualizado[['Margem líquida']] = anualizado[['Margem líquida']].fillna(value=0)


        fig = go.Figure()
        fig.add_bar(name = 'Receita Líquida',y=anualizado['Receita Líquida'],x=anualizado[0],marker_color=colors['receita'],
                    customdata=anualizado[[0,'Crescimento Receita']],
                    hovertemplate="<b>Período</b>: %{x}<br>"+
                    "<b>Receita</b>: R%{y:$,.0}<br>"+
                    "<b>Crescimento</b>: %{customdata[1]:.2%}")

        fig.add_bar(name = 'Custos',y=anualizado['Custos'],x=anualizado[0],marker_color=colors['custos'],
                    hovertemplate="<b>Período</b>: %{x}<br>"+
                    "<b>Custos</b>: R%{y:$,.0}<br>")

        fig.add_scatter(name='Lucro Bruto',y=anualizado['Resultado Bruto'],x=anualizado[0],marker_color=colors['bruto'],
                        customdata=anualizado[[0,'Margem bruta']], 
                        hovertemplate="<b>Período</b>: %{x}<br>"+
                        "<b>Lucro Bruto</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Bruta</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBITDA',y=anualizado['EBITDA'],x=anualizado[0],marker_color=colors['ebitda'],
                        customdata=anualizado[[0,'Margem EBITDA']], 
                        hovertemplate="<b>Período</b>: %{x}<br>"+
                        "<b>EBITDA</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBITDA</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBIT',y=anualizado['EBIT'],x=anualizado[0],marker_color=colors['ebit'], 
                                        customdata=anualizado[[0,'Margem EBIT']], 
                        hovertemplate="<b>Período</b>: %{x}<br>"+
                        "<b>EBIT</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBIT</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='Lucro Líquido',y=anualizado['Lucro Líquido'],x=anualizado[0],marker_color=colors['lucro'], 
                        customdata=anualizado[[0,'Margem líquida']], 
                        hovertemplate="<b>Período</b>: %{x}<br>"+
                        "<b>Lucro Líquido</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Líquida</b>: %{customdata[1]:.2%}")


        fig.update_xaxes(showgrid=True)
        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Demonstração de Resultados Anualizada',template='seaborn',
                         barmode='relative')  

    
    if tipo == 'anual':  
        
        dff = dff.loc[(dff['tipo_resultado'] == tipo)]             
        
        dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])] 

        fig = go.Figure()
        fig.add_bar(name = 'Receita Líquida',y=dff['Receita Líquida'],x=dff['DT_FIM_EXERC'],marker_color=colors['receita'], xperiod="M12",
                    customdata=dff[['LABEL','Crescimento Receita']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Receita</b>: R%{y:$,.0}<br>"+
                    "<b>Crescimento</b>: %{customdata[1]:.2%}")

        fig.add_bar(name = 'Custos',y=dff['Custos'],x=dff['DT_FIM_EXERC'],marker_color=colors['custos'], xperiod="M12",
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Custos</b>: R%{y:$,.0}<br>")

        fig.add_scatter(name='Lucro Bruto',y=dff['Resultado Bruto'],x=dff['DT_FIM_EXERC'],marker_color=colors['bruto'], xperiod="M12",
                        customdata=dff[['LABEL','Margem bruta']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Lucro Bruto</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Bruta</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBITDA',y=dff['EBITDA'],x=dff['DT_FIM_EXERC'],marker_color=colors['ebitda'], xperiod="M12",
                        customdata=dff[['LABEL','Margem EBITDA']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>EBITDA</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBITDA</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBIT',y=dff['EBIT'],x=dff['DT_FIM_EXERC'],marker_color=colors['ebit'], xperiod="M12",
                                        customdata=dff[['LABEL','Margem EBIT']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>EBIT</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBIT</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='Lucro Líquido',y=dff['Lucro Líquido'],x=dff['DT_FIM_EXERC'],marker_color=colors['lucro'], xperiod="M12",
                        customdata=dff[['LABEL','Margem líquida']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Lucro Líquido</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Líquida</b>: %{customdata[1]:.2%}")


        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Demonstração de Resultados Anuais',template='seaborn',
                         barmode='relative')  



    if tipo == 'trimestral':

        dff = dff.loc[(dff['tipo_resultado'] == tipo)]             
        
        dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])] 
        dff.sort_values('DT_FIM_EXERC',inplace=True)
        fig = go.Figure()
        fig.add_bar(name='Receita Líquida',y=dff['Receita Líquida'],x=dff.LABEL,marker_color=colors['receita'],
                    customdata=dff[['LABEL','Crescimento Receita']],
                    hovertemplate="<b>Periodo</b>: %{customdata[0]}<br>"+
                    "<b>Receita</b>: R%{y:$,.0}<br>"+
                    "<b>Crescimento em relação ao ano anterior</b>: %{customdata[1]:.2%}")

        fig.add_bar(name = 'Custos',y=dff['Custos'],x=dff.LABEL,marker_color=colors['custos'],
                    customdata=dff[['LABEL','Crescimento Receita']],
                    hovertemplate="<b>Periodo</b>: %{customdata[0]}<br>"+
                    "<b>Custos</b>: R%{y:$,.0}<br>")

        fig.add_scatter(name='Lucro Bruto',y=dff['Resultado Bruto'], x=dff.LABEL,marker_color=colors['bruto'],
                        customdata=dff[['LABEL','Margem bruta']], 
                        hovertemplate="<b>Periodo</b>: %{customdata[0]}<br>"+
                        "<b>Lucro Bruto</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Bruta</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBITDA',y=dff['EBITDA'],x=dff.LABEL,marker_color=colors['ebitda'],
                        customdata=dff[['LABEL','Margem EBITDA']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>EBITDA</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBITDA</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='EBIT',y=dff['EBIT'],x=dff.LABEL,marker_color=colors['ebit'],
                                        customdata=dff[['LABEL','Margem EBIT']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>EBIT</b>: R%{y:$,.0}<br>"+
                        "<b>Margem EBIT</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='Lucro Líquido',y=dff['Lucro Líquido'],x=dff.LABEL,marker_color=colors['lucro'],
                        customdata=dff[['LABEL','Margem líquida']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Lucro Líquido</b>: R%{y:$,.0}<br>"+
                        "<b>Margem Líquida</b>: %{customdata[1]:.2%}")



        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Demonstração de Resultados Trimestrais',template='seaborn',
                         barmode='relative',bargap= 0.5)  



    if tipo == 'receita stack':

        dff = dff.loc[(dff['tipo_resultado'] == 'trimestral')]             
    
        
        dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])]
        
        df1 = dff
        df1['ano'] = df1['ano'].astype(int)
        df1['ano'] = pd.to_datetime(df1['ano'],format='%Y')
        
        
        # assign colors to type using a dictionary
        colors_tt = {'1 trim':colors['custos'],
                      '2 trim':colors['ebit'],
                      '3 trim':'rgb(248, 181, 0)',
                      '4 trim':colors['receita']}

        # plotly figure
        fig=go.Figure()
        df1.sort_values(['trimestre','ano'],inplace=True)
        
        for t in df1['trimestre'].unique():
            dfp = df1[df1['trimestre']==t]
            

            fig.add_traces(go.Bar(x=dfp['ano'], y = dfp['Receita Líquida'], name=t,
                                 marker_color=colors_tt[t],xperiod='M12'))

            fig.update_xaxes(showgrid=False,ticklabelmode="period", tickformat="%Y")
            fig.update_traces(marker_line_color=colors['contorno'],
                                  marker_line_width=1.5, opacity=0.8)
            fig.update_layout(title_text='Receitas Stacked',template='seaborn',
                             barmode='stack')  
            

    return fig



def dre_indicadores(dff,indicadores,comparadores):

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
        
        
        non_percemt = ['LPA Atual','Giro dos Ativos']
        if any(item in non_percemt for item in indicadores):
            df_indicadores.loc[list(set(non_percemt).intersection(indicadores))] = df_indicadores.loc[list(set(non_percemt).intersection(indicadores))].round(decimals=2).astype(str)
             
       

        df_indicadores.reset_index(inplace=True)
        df_indicadores.rename({'index':''},inplace=True,axis=1)
        
        

        columns=[{"name": i, "id": i, 'type': 'numeric',
                    'format': Format(precision=2, scheme=Scheme.percentage)} for i in df_indicadores.columns]

        columns[0]['editable'] = True

        df_indicadores['id'] = df_indicadores['']
        return  dash_table.DataTable(
                                id="final-table-dre",  fixed_columns={'headers': True,'data': 1},
                                columns=columns,
                                data=df_indicadores.to_dict('records'),
                                row_selectable="single",
                                selected_row_ids=['Margem bruta'],
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



def dre_indicadores_graph(slctd_row_indices,company,year):

    try:
        indic = slctd_row_indices[0]

    except:
        indic = 'Margem bruta'

    d1 = pd.DataFrame.from_dict(company) 
    d1= d1[(d1['tipo_resultado'] == 'anual') | (d1['LABEL'] == 'TTM') ]
      

    try:
        d1['LPA Atual'] = np.nan_to_num(d1['LPA histórico']) + np.nan_to_num(d1['LPA Atual'])
    except:
        d1=d1


    d1 = d1[(d1['ano'] >= year[0]) & (d1['ano'] <= year[1])]
    fig = go.Figure()

    fig.add_bar(showlegend=True,name=indic,y=d1[indic],x=d1['DT_FIM_EXERC'],
                            marker_color=colors['receita'], xperiod="M12",text = d1[indic])
            
        
    if not indic in ['Giro dos Ativos','LPA Atual']:
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
    