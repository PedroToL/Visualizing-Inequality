import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pathlib

from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

dropdown1 = dbc.FormGroup(
    [
        dbc.Label("Country:", html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown-country1",
            options=[
                {"label": "Argentina", "value": 'ARG'},
                {"label": "Bolivia", "value": 'BOL'},
                {"label": "Brazil", "value": 'BRA'},
                {"label": "Chile", "value": 'CHL'},
                {"label": "Colombia", "value": 'COL'},
                {"label": "Costa Rica", "value": 'CRI'},
                {"label": "Dominican Republic", "value": 'DOM'},
                {"label": "Ecuador", "value": 'ECU'},
                {"label": "Guatemala", "value": 'GTM'},
                {"label": "Mexico", "value": 'MEX'},
                {"label": "Peru", "value": 'PER'},
                {"label": "Paraguay", "value": 'PRY'},
                {"label": "El Salvador", "value": 'SLV'},
                {"label": "Uruguay", "value": 'URY'},
            ],
            value='ARG'
        ),
    ]
)
dropdown2 = dbc.FormGroup(
    [
        dbc.Label("Year:", html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown-year1",
            options=[
                {"label": "2018", "value": 2018},
                {"label": "2015", "value": 2015},
                {"label": "2010", "value": 2010},
                {"label": "2005", "value": 2005},
                {"label": "2000", "value": 2000},
            ],
            value=2018
        ),
    ]
)

layout = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dropdown1, lg=6),
                        dbc.Col(dropdown2, lg=6),
                    ]),

                dbc.Card(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                id='pyramid',
                                                className='plot',
                                                config={
                                                    'displaylogo': False
                                                }
                                            ), lg=4),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    dbc.Card(
                                                        [
                                                            html.H2(id='country1'),
                                                            html.Hr(),
                                                            html.P(id='text'),
                                                            html.A('World Factbook', id='link', target="_blank")
                                                        ], id='info', className='c-name')),

                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dcc.Graph(
                                                                id='sexo',
                                                                className='plot',
                                                                config={
                                                                    'displaylogo': False
                                                                }
                                                            ), lg=6),
                                                        dbc.Col(
                                                            dcc.Graph(
                                                                id='zona',
                                                                className='plot-2',
                                                                config={
                                                                    'displaylogo': False
                                                                }
                                                            ), lg=6),
                                                    ], className='bar')
                                            ])
                                    ]),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                id='ingreso',
                                                className='plot',
                                                config={
                                                    'displaylogo': False
                                                }
                                            ), lg=6),
                                        dbc.Col(
                                            dcc.Graph(
                                                id='gini',
                                                className='plot',
                                                config={
                                                    'displaylogo': False
                                                }
                                            ), lg=6)
                                    ], className='row-2')
                            ], className='body')
                    ])
            ], id='main')
    ])


@app.callback(
    [
        Output('country1', 'children'),
        Output('text', 'children'),
        Output('link', 'href'),
        Output('pyramid', 'figure'),
        Output('sexo', 'figure'),
        Output('zona', 'figure'),
        Output('ingreso', 'figure'),
        Output('gini', 'figure'),
    ],
    [
        Input('dropdown-country1', 'value'),
        Input('dropdown-year1', 'value'),
    ]
)
def updateSex(input_value1, input_value2):
    df = pd.read_csv(DATA_PATH.joinpath('pyramid.csv'))
    text = pd.read_excel(DATA_PATH.joinpath('text.xlsx'))
    text_ = text[text['Country'] == input_value1]
    df1 = pd.read_csv(DATA_PATH.joinpath('Rural-Urbano-Sex.csv'))
    df2 = pd.read_csv(DATA_PATH.joinpath('PIB-GINI.csv'))
    dfCHL = df2[df2.country_c == 'CHL']
    dfSLV = df2[df2.country_c == 'SLV']
    dfBID = df2[df2.country_c == 'BID']
    df = df[df.Year == input_value2]
    df1 = df1[df1.year == input_value2]
    df = df[df.Country == input_value1]
    df1 = df1[df1.country_c == input_value1]
    df2 = df2[df2.country_c == input_value1]

    name = df2.country_n.iloc[0]
    text = text_['Situation']
    link = text_['Source'].iloc[0]

    sex = [round(float(df1.female), 2), round(float(df1.male), 2)]
    sex_p = [round(float(df1.female), 2) / 100, round(float(df1.male), 2) / 100]
    zone = [round(float(df1.rural), 2), round(float(df1.urban), 2)]
    zone_p = [round(float(df1.rural), 2) / 100, round(float(df1.urban), 2) / 100]

    women_bins = np.round(list(df.F), 4)
    men_bins = np.round(list(df.M), 4)

    age = list(df['Age Group'])

    layout1 = go.Layout(
        title={
            'text': "Population density",
            'y': .95,
            'x': 0.6,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis=go.layout.YAxis(title='Age'),
        xaxis=go.layout.XAxis(
            range=[-max(abs(men_bins)) - 2, max(women_bins) + 2],
            tickvals=[-10, -5, 0, 5, 10],
            ticktext=['10%', '5%', 0, '5%', '10%'],
            ),
        barmode='overlay',
        bargap=0.2,
        legend=dict(
            orientation="v",
            yanchor="bottom",
            y=.85,
            xanchor="right",
            x=.98),
        template='seaborn',
        margin=dict(l=17, r=0, t=50, b=50),
        annotations=[
            dict(
                x=0,
                y=-0.1,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data1 = [
        go.Bar(
            y=age,
            x=men_bins,
            orientation='h',
            name='Male',
            text=['{}%'.format(round(i, 2) * -1) for i in list(men_bins.astype('float'))],
            hoverinfo='text',
            marker=dict(color='#0931B0'),
            opacity=.7,
        ),
        go.Bar(
            y=age,
            x=women_bins,
            orientation='h',
            name='Female',
            text=['{}%'.format(round(i, 2)) for i in list(women_bins.astype('float'))],
            hoverinfo='text',
            marker=dict(color='#F21857'),
            opacity=.7,
        )
    ]

    trace2 = go.Bar(
        x=['Female', 'Male'],
        y=sex_p,
        text=sex,
        textposition='auto',
        hoverinfo=['y', 'y'],
        marker=dict(color=['#F21857', '#0931B0']),
        opacity=.7,
    )
    layout2 = go.Layout(
        title='Sex',
        margin=dict(l=17, r=0, t=25, b=50),
        height=280,
        template='seaborn',
        yaxis=dict(tickformat=".0%"),
        annotations=[
            dict(
                x=0,
                y=-0.2,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data2 = [trace2, ]

    trace3 = go.Bar(
        x=['Rural', 'Urban'],
        y=zone_p,
        text=zone,
        textposition='auto',
        hoverinfo=['y', 'y'],
        marker=dict(color=['#F21857', '#0931B0']),
        opacity=.7
    )
    layout3 = go.Layout(
        title='Area',
        margin=dict(l=17, r=0, t=25, b=50),
        height=280,
        template='seaborn',
        yaxis=dict(tickformat=".0%"),
        annotations=[
            dict(
                x=0,
                y=-0.2,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data3 = [trace3, ]

    USA1 = go.Scatter(
        x=list(dfCHL.year),
        y=list(dfCHL.GDPpc),
        mode='lines',
        name='Chile',
        line=dict(color='#ea4335'),
        opacity=.5,
        hovertemplate='$%{y:,.2f}',
    )
    BID1 = go.Scatter(
        x=list(dfBID.year),
        y=list(dfBID.GDPpc),
        mode='lines',
        name='Sample mean',
        line=dict(color='#09B07B'),
        opacity=.5,
        hovertemplate='$%{y:,.2f}',
    )
    trace4 = go.Scatter(
        x=list(df2.year),
        y=list(df2.GDPpc),
        mode='lines',
        name=name,
        line=dict(color='#0931B0'),
        hovertemplate='$%{y:,.2f}',
    )
    layout4 = go.Layout(
        title='GDP per Capita' + '<br>' + '<span style="font-size: 12px;">Constant US dollars 2010</span>',
        margin=dict(l=30, r=0, t=60, b=5),
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.35,
            xanchor="right",
            x=1),
        template='seaborn',
        yaxis=dict(tickprefix='$'),
        hovermode='x',
        annotations=[
            dict(
                x=0,
                y=-0.35,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data4 = [trace4, USA1, BID1]

    USA2 = go.Scatter(
        x=list(dfSLV.year),
        y=list(dfSLV.GINI),
        mode='lines',
        name='El Salvador',
        line=dict(color='#ea4335'),
        opacity=.5,
        hovertemplate='%{y:,.2f}',

    )
    BID2 = go.Scatter(
        x=list(dfBID.year),
        y=list(dfBID.GINI),
        mode='lines',
        name='Sample mean',
        line=dict(color='#09B07B'),
        opacity=.5,
        hovertemplate='%{y:,.2f}',

    )
    trace5 = go.Scatter(
        x=list(df2.year),
        y=list(df2.GINI),
        mode='lines',
        name=name,
        line=dict(color='#0931B0'),
        hovertemplate='%{y:,.2f}',

    )
    layout5 = go.Layout(
        title='GINI' + '<br>' + '<span style="font-size: 12px;">From 0 to 100</span>',
        margin=dict(l=17, r=0, t=60, b=5),
        height=300,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-.35,
            xanchor="right",
            x=1),
        template='seaborn',
        hovermode='x',
        annotations=[
            dict(
                x=0,
                y=-0.35,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data5 = [trace5, USA2, BID2]

    return [
        name,
        text,
        link,
        {'data': data1, 'layout': layout1},
        {'data': data2, 'layout': layout2},
        {'data': data3, 'layout': layout3},
        {'data': data4, 'layout': layout4},
        {'data': data5, 'layout': layout5},
    ]
