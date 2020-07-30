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

dropdown_country2 = dbc.FormGroup(
    [
        dbc.Label("Country:", html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown-country3",
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
dropdown_year2 = dbc.FormGroup(
    [
        dbc.Label("Year:", html_for="dropdown"),
        dcc.Dropdown(
            id="dropdown-year3",
            options=[
                {"label": "2018", "value": 2018},
                {"label": "2010", "value": 2010},
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
                        dbc.Col(dropdown_country2, lg=6),
                        dbc.Col(dropdown_year2, lg=6)
                    ]),

                dbc.Card(
                    [
                        dbc.Row(
                            [
                                html.H2(id='country3')
                            ], id='info'),
                        html.Hr(),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id='plot-1_1',
                                        config={
                                            'displaylogo': False
                                        }
                                    ), lg=12
                                )
                            ]),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id='plot-2_1',
                                        config={
                                            'displaylogo': False
                                        }
                                    ), lg=6),
                                dbc.Col(
                                    dcc.Graph(
                                        id='plot-3_1',
                                        config={
                                            'displaylogo': False
                                        }
                                    ), lg=6)
                            ])
                    ], className='body')
            ], id='main')
    ])


@app.callback(
    [
        Output('country3', 'children'),
        Output('plot-1_1', 'figure'),
        Output('plot-2_1', 'figure'),
        Output('plot-3_1', 'figure'),
    ],
    [
        Input('dropdown-country3', 'value'),
        Input('dropdown-year3', 'value'),
    ]
)
def plot1(input_value1, input_value2):
    df1 = pd.read_csv(DATA_PATH.joinpath('page4_.csv'), low_memory=False)
    df2 = pd.read_csv(DATA_PATH.joinpath('pag3.csv'), low_memory=False)
    df1 = df1[df1['country'] == input_value1]
    df2 = df2[df2['country'] == input_value1]
    df2 = df2[df2['year'] == input_value2]

    df_year1 = df1[df1['area'] == 'Urban']
    year1 = []

    for i in range(len(df_year1)):
        year1.append(int((str(df_year1.year.iloc[i]))))

    df_year2 = df1[df1['area'] == 'Rural']
    year2 = []

    for i in range(len(df_year2)):
        year2.append(int((str(df_year2.year.iloc[i]))))

    end = np.percentile(list(df2.income), 99)
    size = end * .015

    trace1 = go.Scatter(
        x=year1,
        y=list(round(df1[df1.area == 'Urban'].income, 2)),
        mode='lines',
        name='Urban',
        line=dict(color='#0931B0'),
        opacity=.7
    )
    trace2 = go.Scatter(
        x=year2,
        y=list(round(df1[df1.area == 'Rural'].income, 2)),
        mode='lines',
        name='Rural',
        line=dict(color='#F21857'),
        opacity=.7
    )
    layout1 = go.Layout(
        title='Income' + '<br>' + '<span style="font-size: 12px;">Local currency (K=1000)</span>',
        margin=dict(l=35, r=5, t=50, b=50),
        height=350,
        template='seaborn',
        yaxis=go.layout.YAxis(
            tickprefix='$',
            tickformat=',.'
        ),
        hovermode='x',
        annotations=[
            dict(
                x=0,
                y=-0.2,
                showarrow=False,
                text="Data Source: IDB",
                xref="paper",
                yref="paper"
            )]
    )
    data1 = [trace1, trace2]

    trace3 = go.Histogram(
        x=df2[df2.area == 'urbana'].educ,
        name='Urban',
        opacity=.5,
        histnorm='probability',
        marker=dict(color='#0931B0')
    )
    trace4 = go.Histogram(
        x=df2[df2.area == 'rural'].educ,
        name='Rural',
        opacity=.5,
        histnorm='probability',
        marker=dict(color='#F21857')
    )
    layout2 = go.Layout(
        title='Years of Education',
        barmode='group',
        margin=dict(l=30, r=0, t=30, b=50),
        height=300,
        template='seaborn',
        xaxis=go.layout.XAxis(
            title='Years',
            tickvals=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        ),
        yaxis=go.layout.YAxis(
            tickformat='.0%'
        ),
        hovermode='x',
        annotations=[
            dict(
                x=0,
                y=-0.2,
                showarrow=False,
                text="Data Source: IDB",
                xref="paper",
                yref="paper"
            )]
    )
    data2 = [trace3, trace4]

    trace5 = go.Histogram(
        x=df2[df2.area == 'urbana'].income,
        name='Urban',
        opacity=.5,
        histnorm='probability',
        xbins=dict(  # bins used for histogram
            start=0,
            end=end,
            size=size
        ),
        autobinx=False,
        marker=dict(color='#0931B0'),
        hovertemplate='%{y:.2%}<extra></extra>',
    )
    trace6 = go.Histogram(
        x=df2[df2.area == 'rural'].income,
        name='Rural',
        opacity=.5,
        histnorm='probability',
        xbins=dict(  # bins used for histogram
            start=0,
            end=end,
            size=size
        ),
        autobinx=False,
        marker=dict(color='#F21857'),
        hovertemplate='%{y:.2%}<extra></extra>',
    )
    layout3 = go.Layout(
        title='Income Distribution',
        barmode='overlay',
        margin=dict(l=30, r=0, t=30, b=50),
        height=300,
        template='seaborn',
        yaxis=go.layout.YAxis(
            tickformat='.0%'
        ),
        xaxis=go.layout.XAxis(
            tickprefix='$',
            title='Income'
        ),
        hovermode='x',
        annotations=[
            dict(
                x=0,
                y=-0.2,
                showarrow=False,
                text="Data Source: IDB",
                xref="paper",
                yref="paper"
            )]
    )
    data3 = [trace5, trace6]

    name = df1['c_name'].iloc[0]

    return [
        name,
        {'data': data1, 'layout': layout1},
        {'data': data2, 'layout': layout2},
        {'data': data3, 'layout': layout3},
    ]
