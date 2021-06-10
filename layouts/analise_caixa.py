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

indicadores = [ 'Capital_Giro/revenues',
                'Capex/Receita',
                'Capex/Depreciação',
                'Capex Líquido/Receita',
                'Capex Líquido/EBIT(1-t)',
                'P/Cap_Giro Atual',
                'Porcentagem Reinvestida']

def layout_tab4(df):
    return html.Div([
                
                     dbc.Container([ ## fluxo de caixa 
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Demonstração do Fluxo de Caixa"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dfc_table',
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
                                                            html.Div(
                                                                    id="dfc_table")],
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
                                                dbc.CardHeader("Análise Gráfica Atividades de Investimento"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_dfc_graph",
                                                                options=[{'label': 'Capex','value': 'capex'},
                                                                        {'label': 'Capital de Giro (non-cash)', 'value': 'wc_non_cash'},  
                                                                        ],
                                                                value='capex',
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dfc_graph',
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
                                                                    children=[dcc.Graph(id="dfc_graph")]
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
                                                                id="dropdown_indicadores_dfc",
                                                                options=[{"label": x, "value": x} for x in indicadores],
                                                                multi=True,
                                                                value=['Capital_Giro/revenues',
                                                                        'Capex/Receita'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                    id='dropdown_comparador_dfc',
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
                                                                    id="indicadores_dfc_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_dfc_indic',
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
                                                                            children=[dcc.Graph(id='dfc_indicadores_graph')]
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



def layout_dfc_table(dff,year):


    dff = dff.loc[(dff['tipo_resultado'] == 'anual')]             
    
            
        
    dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])]
    

    dfc = dff.sort_values(by='DT_FIM_EXERC')
    dfc1 = dfc.pivot_table(columns=['ano','LABEL'], values=['Aumento (Redução) de Caixa e Equivalentes',
                                                            'Caixa Gerado nas Operações',
                                                            'Caixa Líquido Atividades Operacionais',
                                                            'Caixa Líquido Atividades de Financiamento',
                                                            'Caixa Líquido Atividades de Investimento',
                                                            'Capex',
                                                            'Saldo Final de Caixa e Equivalentes',
                                                            'Saldo Inicial de Caixa e Equivalentes',
                                                            'Variação Cambial s/ Caixa e Equivalentes',
                                                            'Variações nos Ativos e Passivos',
                                                            'Depreciação'])

    index_order = ['Caixa Líquido Atividades Operacionais',
                    'Caixa Gerado nas Operações',
                    'Depreciação',
                    'Variações nos Ativos e Passivos',
                    'Caixa Líquido Atividades de Investimento',
                    'Capex',
                    'Caixa Líquido Atividades de Financiamento',
                    'Variação Cambial s/ Caixa e Equivalentes',
                    'Aumento (Redução) de Caixa e Equivalentes',
                    'Saldo Inicial de Caixa e Equivalentes',
                    'Saldo Final de Caixa e Equivalentes']

    dfc3 = dfc1.reindex(index_order)

    dfc3 = dfc3[dfc3.columns[::-1]]
    dfc3.reset_index(inplace=True)
    dfc3.columns = dfc3.columns.droplevel(0)
    

    ahs = []
    for x in range(1,(len(dfc3.columns)-1)):
        data = (dfc3[dfc3.columns[x]]-dfc3[dfc3.columns[x+1]])/np.abs(dfc3[dfc3.columns[x+1]])
        ahs.append(data)

    y = 0
    for x in range(2,(len(dfc3.columns)+len(ahs)-1),2):

        dfc3.insert(x,'AH_%i'%y,ahs[y])
        y=y+1

    columns = [{'name': '', 'id': '', 'type': 'text', 'editable': True}]
    formatation = []
    for x in range(1,(len(dfc3.columns))):
        if (x % 2) == 0:
            columns.append({"name": 'AH %', "id": dfc3.columns[x],'type':'numeric',
                  'format': Format(precision=2, scheme=Scheme.percentage),
                            'hideable': True})
            formatation.append(dfc3.columns[x])

        else:
            columns.append({"name": dfc3.columns[x], "id": dfc3.columns[x],'type':'numeric',
                  'format': Format(precision=2,group=',',group_delimiter='.',
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                    si_prefix=Prefix.mega, symbol_suffix=' ')})
    
  
    
    red_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} < 0'.format(x)},
        'color': 'red'}  for x in formatation]
    
    green_values = [{'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 0'.format(x)},
        'color': 'green'}  for x in formatation]

    red_values.extend(green_values)

    return ([dash_table.DataTable(
                            id="final-table-2",  fixed_columns={'headers': True,'data': 1},
                            columns=columns,
                            data=dfc3.to_dict('records'),   
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



def dfc_graph(dff,tipo,year):

    dff = dff.loc[(dff['tipo_resultado'] == 'anual')]             
        
    dff = dff[(dff['ano'] >= year[0]) & (dff['ano'] <= year[1])] 
 
    dff.sort_values('DT_FIM_EXERC', inplace=True)

    dff[['Capex']] = dff[['Capex']].fillna(value=0)
    dff[['Capex/Receita']] = dff[['Capex/Receita']].fillna(value=0)
    dff[['Depreciação']] = dff[['Depreciação']].fillna(value=0)
    dff[['Capex Líquido']] = dff[['Capex Líquido']].fillna(value=0)
    dff[['Capex Líquido/Receita']] = dff[['Capex Líquido/Receita']].fillna(value=0)
    dff[['Capex Líquido/EBIT(1-t)']] = dff[['Capex Líquido/EBIT(1-t)']].fillna(value=0)
    dff[['Capital de Giro non-cash']] = dff[['Capital de Giro non-cash']].fillna(value=0)
    dff[['Variação Capital de Giro']] = dff[['Variação Capital de Giro']].fillna(value=0)
    dff[['Capital_Giro/revenues']] = dff[['Capital_Giro/revenues']].fillna(value=0)
    dff[['Patrimônio Reinvestido']] = dff[['Patrimônio Reinvestido']].fillna(value=0)
    dff[['Porcentagem Reinvestida']] = dff[['Porcentagem Reinvestida']].fillna(value=0)

    if tipo == 'capex':

        fig = go.Figure()
        fig.add_bar(name = 'CAPEX',y=dff['Capex'],x=dff['DT_FIM_EXERC'],marker_color=colors['receita'], xperiod="M12",
                    customdata=dff[['LABEL','Capex/Receita']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Capex</b>: R%{y:$,.0}<br>"+
                    "<b>Capex/Receita</b>: %{customdata[1]:.2%}")
    
        fig.add_scatter(name='Depreciação',y=dff['Depreciação'],x=dff['DT_FIM_EXERC'],marker_color=colors['bruto'], xperiod="M12",
                        customdata=dff[['LABEL','Capex/Depreciação']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Depreciação</b>: R%{y:$,.0}<br>"+
                        "<b>Capex/Depreciação</b>: %{customdata[1]:.2%}")

        fig.add_scatter(name='Capex Líquido',y=dff['Capex Líquido'],x=dff['DT_FIM_EXERC'],marker_color=colors['ebitda'], xperiod="M12",
                        customdata=dff[['LABEL','Capex Líquido/Receita','Capex Líquido/EBIT(1-t)']], 
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Capex Líquido</b>: R%{y:$,.0}<br>"+
                        "<b>Capex Líquido/Receita</b>: %{customdata[1]:.2%}<br>"+
                        "<b>Capex Líquido/EBIT(1-t)</b>: %{customdata[2]:.2%}")

        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Atividades de Investimento (CAPEX)',template='seaborn',
                         barmode='relative')


    if tipo == 'wc_non_cash':

        fig = go.Figure()
        fig.add_bar(name = 'Capital de Giro (non-cash)',y=dff['Capital de Giro non-cash'],x=dff['DT_FIM_EXERC'],marker_color=colors['receita'], xperiod="M12",
                    customdata=dff[['LABEL','Capital_Giro/revenues']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Capital de Giro NC</b>: R%{y:$,.0}<br>"+
                    "<b>Capital_Giro/Receitas</b>: %{customdata[1]:.2%}")
    
        fig.add_scatter(name='Variação do Capital de giro',y=dff['Variação Capital de Giro'],x=dff['DT_FIM_EXERC'],marker_color=colors['bruto'], xperiod="M12",
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                        "<b>Variação Capital de Giro</b>: R%{y:$,.0}<br>")


        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Capital de Giro (non-cash)',template='seaborn',
                         barmode='relative')


    if tipo == 'patri_reinv':

        fig = go.Figure()
        fig.add_bar(name = 'Patrimônio Reinvestido',y=dff['Patrimônio Reinvestido'],x=dff['DT_FIM_EXERC'],marker_color=colors['receita'], xperiod="M12",
                    customdata=dff[['LABEL','Porcentagem Reinvestida']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                    "<b>Patrimônio Reinvestido</b>: R%{y:$,.0}<br>"+
                    "<b>Porcentagem Reinvestida</b>: %{customdata[1]:.2%}")

        fig.update_xaxes(showgrid=True,ticklabelmode="period",  tickformat="%Y")
        fig.update_traces(marker_line_color=colors['contorno'],
                              marker_line_width=1.5, opacity=0.8)
        fig.update_layout(title_text='Patrimônio Reinvestido',template='seaborn',
                         barmode='relative')


    return fig



def dfc_indicadores(dff,indicadores,comparadores):

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
        
        
        non_percemt =['P/Cap_Giro Atual']
        if any(item in non_percemt for item in indicadores):
            df_indicadores.loc[list(set(non_percemt).intersection(indicadores))] = df_indicadores.loc[list(set(non_percemt).intersection(indicadores))].round(decimals=2).astype(str)
            



        df_indicadores.reset_index(inplace=True)
        df_indicadores.rename({'index':''},inplace=True,axis=1)
        
        

        columns=[{"name": i, "id": i, 'type': 'numeric',
                    'format': Format(precision=2, scheme=Scheme.percentage)} for i in df_indicadores.columns]

        columns[0]['editable'] = True

        df_indicadores['id'] = df_indicadores['']
        return  dash_table.DataTable(id='final-table-dfc',fixed_columns={'headers': True,'data': 1},
                                columns=columns,
                                data=df_indicadores.to_dict('records'),
                                row_selectable="single",
                                selected_row_ids=['Capex/Receita'],
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



def dfc_indicadores_graph(slctd_row_indices,company,year):

    try:
        indic = slctd_row_indices[0]

    except:
        indic = 'Capital_Giro/revenues'


    d1 = pd.DataFrame.from_dict(company) 
    d1= d1[(d1['tipo_resultado'] == 'anual') | (d1['LABEL'] == 'TTM') ]  
    

    try:
        d1['P/Cap_Giro Atual'] = np.nan_to_num(d1['P/Cap_Giro histórico']) + np.nan_to_num(d1['P/Cap_Giro Atual'])
    except:
        d1=d1

    d1 = d1[(d1['ano'] >= year[0]) & (d1['ano'] <= year[1])]
    fig = go.Figure()

    fig.add_bar(showlegend=True,name=indic,y=d1[indic],x=d1['DT_FIM_EXERC'],
                            marker_color=colors['receita'], xperiod="M12",text = d1[indic])
            
        
    if not indic in ['P/Cap_Giro Atual']:
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
    