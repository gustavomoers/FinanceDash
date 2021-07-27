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
from plotly.subplots import make_subplots

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
    alldiv = pd.read_pickle(DATA_PATH.joinpath('proventos_b3.pkl'))  # GregorySmith Kaggle

colors = {'header': "rgb(144, 31, 35)",'first_column': 'rgb(190, 195, 218,.2)',
          'column_ttm': 'rgb(248, 181, 0,.3)','head_table':'rgb(190, 195, 218,.5)',
          'receita': 'rgb(144, 31, 35)','custos': 'rgb(61, 174, 254)','bruto' :'rgb(38,38,38)',
          'ebitda':'rgb(133, 204, 254)','ebit':'rgb(98, 112, 167)','lucro':'rgb(248, 181, 0)',
          'contorno':'rgb(8,48,107)'}

indicadores = ['Dividend Yield','Payout']

def layout_tab6():
    return html.Div([
                
                     dbc.Container([ ## tabela proventos
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            [
                                                dbc.CardHeader("Proventos Históricos"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            html.Div(
                                                                    id="div_table")],
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
                                                dbc.CardHeader("Análise Gráfica Proventos"),
                                                dbc.CardBody([
                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id="dropdown_div_graph",
                                                                options=[{'label': 'Proventos','value': 'provento'},
                                                                            {'label': 'Proventos por Ano', 'value': 'ano'},
                                                                            {'label': 'Payout', 'value': 'payout'},
                                                                        ],
                                                                value='ano',
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_div_graph',
                                                                    updatemode = 'mouseup',
                                                                    min=2006,
                                                                    max=int(this_year),
                                                                    value=[2016,int(this_year)],
                                                                    marks={year: str(year) for year in range(2006,int(this_year)+1,2)},
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
                                                                    children=[dcc.Graph(id="div_graph")]
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
                                                                id="dropdown_indicadores_div",
                                                                options=[{"label": x, "value": x} for x in indicadores],
                                                                multi=True,
                                                                value=['Dividend Yield','Payout'],
                                                                persistence=True,
                                                                persistence_type='session',
                                                                style={'margin': 'left','font-family':'sans-serif',
                                                                        'fontSize':12})
                                                                ],width={'size': 4, 'offset': 0},
                                                            ),

                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                    id='dropdown_comparador_div',
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
                                                                    id="indicadores_div_table")],
                                                                    width={'size': 12, 'offset': 0},
                                                            ),
                                                    ]),

                                                    html.Br(),

                                                    dbc.Row([
                                                        dbc.Col([
                                                            dcc.RangeSlider(
                                                                    id='slider_div_indic',
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
                                                                            children=[dcc.Graph(id='div_indicadores_graph')]
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



def layout_div_table(dff):

    cd_cv = dff['Codigo_CVM'].unique()[0]
    tipo = dff['CLASSE_x'].unique()[0]

    medias = Medias()

    d1 = getattr(medias,'alldiv')

    diviid = d1.query("Codigo_CVM == [@cd_cv]")

    if tipo == 'UNT N2':
        tipo = 'UNT'

    diviid = diviid.loc[(diviid['CLASSE'] == tipo)]

    diviid = diviid.loc[(diviid['Proventos'].isin(['DIVIDENDO','JRS CAP PROPRIO']))]

    diviid.drop(diviid.columns.difference(['Proventos','Data COM','Valor',
       'Valor ajustado', 'Preço COM ajustado', 'Provento/Preço(%) ajustado','Pagamento']),axis=1,inplace=True)

    diviid['Data COM'] = pd.to_datetime(diviid['Data COM'],errors='coerce')
    diviid['Pagamento'] = pd.to_datetime(diviid['Pagamento'],errors='coerce')

    diviid.sort_values('Data COM',inplace=True,ascending=False)

    diviid['Data COM'] = diviid['Data COM'].dt.strftime('%d-%m-%Y')
    diviid['Pagamento'] = diviid['Pagamento'].dt.strftime('%d-%m-%Y')

    diviid = diviid[['Proventos','Data COM','Pagamento','Valor','Valor ajustado','Preço COM ajustado',
                    'Provento/Preço(%) ajustado']]
    
    columns = [{'name': 'Proventos', 'id': 'Proventos', 'type': 'text', 'editable': True,'hideable':True},
             {'name': 'Data COM', 'id': 'Data COM', 'hideable': True},
             {'name': 'Pagamento', 'id': 'Pagamento', 'hideable': True},
             {'name': 'Valor', 'id': 'Valor', 'hideable': True, 'type':'numeric',
                  'format': Format(precision=4,
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                    symbol_suffix=' ')},
             {'name': 'Valor ajustado', 'id': 'Valor ajustado', 'hideable': True,'type':'numeric',
                  'format': Format(precision=4,
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                     symbol_suffix=' ')},
             {'name': 'Preço COM ajustado', 'id': 'Preço COM ajustado', 'hideable': True, 'type':'numeric',
                  'format': Format(precision=4,
                    decimal_delimiter=',',symbol=Symbol.yes, symbol_prefix='R$ ',
                     symbol_suffix=' ')},
             {'name': 'Provento/Preço(%) ajustado',
              'id': 'Provento/Preço(%) ajustado',
              'hideable': True,'type':'numeric',
                  'format': Format(precision=2, scheme=Scheme.percentage)}]


    return ([dash_table.DataTable(
                            id="final-table-4",  fixed_columns={'headers': True},
                            columns=columns,
                            data=diviid.to_dict('records'),   
                            style_table={'minWidth': '100%','marginLeft': 'auto', 
                                         'marginRight': 'auto'},
                            style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto'},
                            style_cell={
                                        'height': 'auto',
                                        # all three widths are needed
                                        'minWidth': '80px', 'width': '80px', 'maxWidth': '80px',
                                        'whiteSpace': 'normal','font-family':'sans-serif',
                                        'fontSize':12,
                                    },
        
                            style_cell_conditional=[{
                                                    'if': {'column_id': 'Proventos'},
                                                    'width': '100px','textAlign':'left',
                                                    'fontWeight': 'bold'},
                                                    {'if': {'column_id': 'TTM'},
                                                            'backgroundColor': colors['column_ttm']}
                                                ],

                            style_header={
                                        'backgroundColor': colors['head_table'],
                                        'fontWeight': 'bold','textAlign': 'center'
                                    },

                            style_as_list_view=True,
                            export_format='xlsx',
                            export_headers='display',
                            merge_duplicate_headers=True,page_size=10
                            )])



def div_graph(dff,tipo,year):

    if tipo == 'provento':
        cd_cv = dff['Codigo_CVM'].unique()[0]
        tipo = dff['CLASSE_x'].unique()[0]

        medias = Medias()

        d1 = getattr(medias,'alldiv')

        diviid = d1.query("Codigo_CVM == [@cd_cv]")

        if tipo == 'UNT N2':
            tipo = 'UNT'

        diviid = diviid.loc[(diviid['CLASSE'] == tipo)]

        diviid = diviid.loc[(diviid['Proventos'].isin(['DIVIDENDO','JRS CAP PROPRIO']))]

        diviid['Data COM'] = pd.to_datetime(diviid['Data COM'])

        diviid['Data COM'] = diviid['Data COM'].dt.strftime('%d-%m-%Y')

        diviid = diviid[(diviid['ano'] >= year[0]) & (diviid['ano'] <= year[1])]

        diviid['Provento/Preço(%) ajustado'].replace(np.nan,0,inplace=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_bar(name='Proventos',y=diviid['Valor ajustado'],x=diviid['Data COM'],
                customdata=diviid[['Pagamento','Provento/Preço(%) ajustado']],
                hovertemplate="<b>Data</b>: %{x}<br>"+
                        "<b>Provento</b>: R%{y:$,.4f}<br>"+"<b>DY</b>: %{customdata[1]:.2%}",
                marker_color=colors['receita'],secondary_y=False)

        fig.add_scatter(name='Preço Data COM',y=diviid['Preço COM ajustado'],x=diviid['Data COM'],
                    customdata=diviid[['Pagamento','Provento/Preço(%) ajustado']],
                    hovertemplate="<b>Data</b>: %{x}<br>"+
                        "<b>Preço</b>: R%{y:$,.2f}<br>"+"<b>DY</b>: %{customdata[1]:.2%}",
                    marker_color=colors['lucro'],secondary_y=True)

        fig.update_xaxes(showgrid=False,type="category")      


    if tipo == 'ano':

        df1 = dff.loc[(dff['tipo_resultado'] == 'anual') | (dff['LABEL'] == 'TTM')]
        df1 = df1[(df1['ano'] >= year[0]) & (df1['ano'] <= year[1])]
        df1.sort_values('DT_FIM_EXERC', inplace=True)

        df1[['Preço']] = df1[['Preço']].fillna(value=0)
        df1[['Dividend Yield']] = df1[['Dividend Yield']].fillna(value=0)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_bar(name='Proventos',y=df1['Proventos no Período'],x=df1['LABEL'],
                    customdata=df1[['LABEL','Dividend Yield']],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                            "<b>Soma Proventos</b>: R%{y:$,.4f}<br>"+"<b>DY</b>: %{customdata[1]:.2%}",
                    marker_color=colors['receita'], xperiod="M12",secondary_y=False)

        fig.add_scatter(name='Preço Final do Período',y=df1['Preço'],x=df1['LABEL'],
                        customdata=df1[['LABEL','Dividend Yield']],
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                            "<b>Preço</b>: R%{y:$,.2f}<br>"+"<b>DY</b>: %{customdata[1]:.2%}",
                        marker_color=colors['lucro'],secondary_y=True)

        fig.update_xaxes(showgrid=False,ticklabelmode="period",  tickformat="%Y")


    
    if tipo == 'payout':

        df1 = dff.loc[(dff['tipo_resultado'] == 'anual') | (dff['LABEL'] == 'TTM')]

        df1 = df1[(df1['ano'] >= year[0]) & (df1['ano'] <= year[1])]

        df1.sort_values('DT_FIM_EXERC', inplace=True)

        df1[['Preço']] = df1[['Preço']].fillna(value=0)
        df1[['Dividend Yield']] = df1[['Dividend Yield']].fillna(value=0)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_bar(name='Proventos',y=df1['Proventos'],x=df1['LABEL'],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                            "<b>Proventos</b>: R%{y:$,.2f}<br>",
                    marker_color=colors['receita'], xperiod="M12",secondary_y=False)


        fig.add_bar(name='Lucro Líquido',y=df1['Lucro Atribuído a Controladores'],x=df1['LABEL'],
                    hovertemplate="<b>Ano</b>: %{x}<br>"+
                            "<b>Lucro</b>: R%{y:$,.2f}<br>",
                    marker_color=colors['custos'], xperiod="M12",secondary_y=False)


        fig.add_scatter(name='Payout',y=df1['Payout'],x=df1['LABEL'],
                        hovertemplate="<b>Ano</b>: %{x}<br>"+
                            "<b>Payout</b>: %{y:.2%}<br>",
                        marker_color=colors['lucro'],secondary_y=True)

        fig.update_xaxes(showgrid=False,ticklabelmode="period",  tickformat="%Y")



    return fig



def div_indicadores(dff,indicadores,comparadores):

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
        
      
        df_indicadores.reset_index(inplace=True)
        df_indicadores.rename({'index':''},inplace=True,axis=1)
        
        

        columns=[{"name": i, "id": i, 'type': 'numeric',
                    'format': Format(precision=2, scheme=Scheme.percentage)} for i in df_indicadores.columns]

        columns[0]['editable'] = True

        df_indicadores['id'] = df_indicadores['']
        return  dash_table.DataTable(
                                id="final-table-div",  fixed_columns={'headers': True,'data': 1},
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



def div_indicadores_graph(slctd_row_indices,company,year):

    try:
        indic = slctd_row_indices[0]

    except:
        indic = 'Dividend Yield'

    d1 = pd.DataFrame.from_dict(company) 
    d1= d1[(d1['tipo_resultado'] == 'anual') | (d1['LABEL'] == 'TTM') ]
      


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
    