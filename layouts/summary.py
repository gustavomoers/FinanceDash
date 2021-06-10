import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import locale
locale.setlocale(locale.LC_ALL, '')



def summary_name(nome_empresarial='-',cnpj='-',pagina_web='-'):
    return html.Div([dbc.Row(
                            html.H4(nome_empresarial,
                                style={'font-weight':'bold'}
                                ),
                        ), 
                    dbc.Row(
                            html.P(cnpj,
                                    ),
                        ),
                    dbc.Row(
                            html.A(html.Button('Página Empresa',
                            style={
                                    'color': 'rgb(12, 11, 11)',
                                    'background-color': 'rgb(190, 195, 218)',
                                    'border-color': 'rgb(144, 31, 35)',
                                    'display': 'inline-block',
                                    'font-weight': '200',
                                    'text-align': 'center',
                                    'white-space': 'nowrap',
                                    'vertical-align': 'middle',
                                    '-webkit-user-select': 'none',
                                    '-moz-user-select': 'none',
                                    '-ms-user-select': 'none',
                                    'user-select': 'none',
                                    'border': '1px rgb(144, 31, 35) solid',
                                    'padding': '.375rem .75rem',
                                    'font-size': '.9rem',
                                    'line-height': '1.5',
                                    'border-radius': '.25rem',
                                },
                                ), href=pagina_web, target="_blank"
                            ),
                        ),
                    ])


def summary_table_setor(setor='-',subsetor='-',segmento='-',class_capital='-',world='-'):
        return html.Div([
                dbc.Table(
                                html.Tbody([
                                                html.Tr([html.Td("Setor",
                                                        style={'font-weight': 'bold'}), 
                                                html.Td(setor,
                                                        style={'text-align': 'right'})]),
                                                html.Tr([html.Td("Sub-setor",
                                                        style={'font-weight': 'bold'}), 
                                                html.Td(subsetor,
                                                        style={'text-align': 'right'})]),
                                                html.Tr([html.Td("Segmento",
                                                        style={'font-weight': 'bold'}), 
                                                html.Td(segmento,
                                                        style={'text-align': 'right'})]),
                                                html.Tr([html.Td("Classificação Capital",
                                                        style={'font-weight': 'bold'}), 
                                                html.Td(class_capital,
                                                        style={'text-align': 'right'})]),  
                                                html.Tr([html.Td("Classificação Global:",
                                                        style={'font-weight': 'bold'}), 
                                                html.Td(world,
                                                        style={'text-align': 'right'})],
                                                ),
                                                        
                                                        
                                        ]),
                                                striped=True, bordered=False, hover=True),
                ],
                )


def summary_table_first(codigos='-',seg_b3='-',price = 0,total_papeis = 0,total_on = 0,total_pn = 0,mv_value = 0):
    
    return html.Div([
                    dbc.Table(
                            html.Tbody([
                                        html.Tr([html.Td("Códigos",
                                                 style={'font-weight': 'bold'}), 
                                        html.Td(codigos,
                                                style={'text-align': 'right'})]),
                                        html.Tr([html.Td("Preço Atual",
                                                style={'font-weight': 'bold'}), 
                                        html.Td(locale.currency(price, grouping=True),
                                                style={'text-align': 'right'})]),
                                        html.Tr([html.Td("Número de Papéis",
                                                style={'font-weight': 'bold'}), 
                                        html.Td(locale.format_string('%.0f',total_papeis, grouping=True),
                                                style={'text-align': 'right'})],
                                               title="Total ON: "+
                                                locale.format_string('%.0f',total_on, grouping=True)+'    '+
                                                    "Total PN: "+locale.format_string('%.0f',total_pn, grouping=True)),
                                        html.Tr([html.Td("Valor de Mercado",
                                                style={'font-weight': 'bold'}), 
                                        html.Td(locale.currency(mv_value, grouping=True),
                                                style={'text-align': 'right'})]),  
                                        html.Tr([html.Td("Segmento B3",
                                                 style={'font-weight': 'bold'}), 
                                        html.Td(seg_b3,
                                                style={'text-align': 'right'})]),
                                                
                                                 
                                    ]),
                                        striped=True, bordered=False, hover=True),
                            ]
                    )