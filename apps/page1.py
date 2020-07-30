import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash_table import DataTable
import plotly.graph_objects as go
import pandas as pd
import pathlib

from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

print(DATA_PATH.joinpath('page1.csv'))

df = pd.read_csv(DATA_PATH.joinpath('page1.csv'))
df = df[df['c_code'] != 'OED']

years = list(df['year'].unique())
regions = list(df['region'].unique())

fig_dict = {
    'data': [],
    'layout': {},
    'frames': []
}
fig_dict["layout"]["xaxis"] = {"range": [min(df['GDP_PC_2010']) - 500, max(df['GDP_PC_2010']) + 500],
                               "title": "GDP per Capita (US$ 2010)"}
fig_dict["layout"]["yaxis"] = {"title": "Urban-rural ratio",
                               "range": [-2, max(df['ratio']) + 1]}
fig_dict["layout"]["hovermode"] = "closest"

fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

year = 1999
for region in regions:
    dataset_by_year = df[df["year"] == year]
    dataset_by_year_and_reg = dataset_by_year[
        dataset_by_year["region"] == region]

    data_dict = {
        "x": list(dataset_by_year_and_reg["GDP_PC_2010"]),
        "y": list(dataset_by_year_and_reg["ratio"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_reg["c_name"]),
        "marker": {
            "sizemode": "area",
            "sizeref": .1,
            "size": list(dataset_by_year_and_reg["density"].astype(float)),
        },
        'hovertemplate':
            "<b>%{text}</b><br><br>" +
            "GDP per Capita: %{x:$,.1f}<br>" +
            "Ratio: %{y:.1f}<br>" +
            "Density: %{marker.size:,.1f} -per sq. Km" +
            "<extra></extra>",
        "name": region
    }
    fig_dict["data"].append(data_dict)

for year in years:
    frame = {"data": [], "name": str(year)}
    for region in regions:
        dataset_by_year = df[df["year"] == int(float(year))]
        dataset_by_year_and_reg = dataset_by_year[
            dataset_by_year["region"] == region]

        data_dict = {
            "x": list(dataset_by_year_and_reg["GDP_PC_2010"]),
            "y": list(dataset_by_year_and_reg["ratio"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_reg["c_name"]),
            "marker": {
                "sizemode": "area",
                "sizeref": .1,
                "size": list(dataset_by_year_and_reg["density"].astype(float))
            },
            'hovertemplate':
                "<b>%{text}</b><br><br>" +
                "GDP per Capita: %{x:$,.1f}<br>" +
                "Ratio: %{y:.1f}<br>" +
                "Density: %{marker.size:,.1f} -per sq. Km" +
                "<extra></extra>",
            "name": region
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": str(year),
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]

fig1 = go.Figure(fig_dict)

fig1.update_layout(
    title='Evolution of GDP per Capita, Urban-Rural Ratio and Population Density <br> <span style="font-size: 12;">('
          'K=1000)</span>',
    template='seaborn',
    colorway=['#0931B0', '#09B07B', '#F21857'],
    margin=dict(r=5, l=5, t=50, b=0),
    yaxis=dict(tickformat=".2f"),
    xaxis=dict(tickprefix="$"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.2,
        xanchor="right",
        x=1),
    annotations=[
        dict(
            x=0,
            y=-0.15,
            showarrow=False,
            text="Data Source: World Bank",
            xref="paper",
            yref="paper"
        )]
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='plot1',
                            figure=fig1,
                            config={
                                'displaylogo': False
                            }
                        )
                    ]
                )
            ]
        ),
        html.Hr(className='divi'),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("Year:", html_for="dropdown", id='label'),
                                dcc.Dropdown(
                                    id="years",
                                    options=[{'label': str(i), 'value': i} for i in range(2000, 2019)],
                                    value=2018
                                ),
                                dbc.RadioItems(
                                    options=[
                                        {"label": "GDP per Capita", "value": 1},
                                        {"label": "Population density", "value": 2},
                                        {"label": "Ratio", "value": 3},
                                    ],
                                    value=1,
                                    id="radioitems-input",
                                    inline=True,
                                    className='lg'
                                ),

                            ]
                        ),
                    ], id="page1-2"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='plot2',
                            config={
                                'displaylogo': False
                            }
                        )
                    ]
                )
            ], id='row-2'
        ),
        html.Hr(className='divi'),
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("Year:", html_for="dropdown", id='label2'),
                                dcc.Dropdown(
                                    id="years1",
                                    options=[{'label': str(i), 'value': i} for i in range(1999, 2019)],
                                    value=2018
                                ),
                            ]
                        ),
                    ], id="page1-3"
                )
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        DataTable(
                            id='table',
                            columns=[
                                {'id': 'c_name', 'name': 'Country'},
                                {'id': 'GDP_PC_2010', 'name': 'GDP per Capita (constant US$ 2010)', 'type': 'numeric'},
                                {'id': 'ratio', 'name': 'Urban-Rural Ratio', 'type': 'numeric'},
                                {'id': 'density', 'name': 'Population Density', 'type': 'numeric'}
                            ],
                            editable=False,
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current=0,
                            page_size=16,
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['c_name', ]
                            ],
                            style_cell={
                                'height': 'auto',
                                'whiteSpace': 'normal',
                            }
                        )
                    ]
                )
            ]
        )
    ], id='page1'
)


@app.callback(
    [
        Output('plot2', 'figure'),
        Output('table', 'data')
    ],
    [
        Input('years', 'value'),
        Input('radioitems-input', 'value'),
        Input('years1', 'value'),
    ]
)
def updatePage_1(input_value, radio_value, input_value2):
    df1 = pd.read_csv(DATA_PATH.joinpath('page1.csv'))

    if radio_value == 1:
        df1['y'] = df1['GDP_PC_2010'].astype(float)
        title = 'GDP per Capita' + '<br>' + '<span style="font-size: 12;">constant US$ 2010</span>'
        yaxis = dict(tickprefix='$')
    elif radio_value == 2:
        df1['y'] = df1['density'].astype(float)
        title = 'Population density' + '<br>' + '<span style="font-size: 12;">per sq. Km</span>'
        yaxis = dict(ticksuffix='', tickprefix='')
    elif radio_value == 3:
        df1['y'] = df1['ratio'].astype(float)
        title = 'Urban-Rural' + '<br>' + '<span style="font-size: 12;">% ratio</span>'
        yaxis = dict()

    df2 = df1[df1['year'] == input_value]
    df3 = df2.sort_values(by="y", ascending=False)

    df_table = df1[df1['year'] == input_value2]
    df_table['density'] = round(df_table['density'], 2)
    df_table['ratio'] = round(df_table['ratio'], 2)
    df_table['GDP_PC_2010'] = round(df_table['GDP_PC_2010'], 2)

    df_table = df_table.sort_values(by="c_name")

    colors = ['#F21857' if i == 'OECD members' else '#0931B0' for i in df3['c_name']]

    trace = go.Bar(
        x=df3['c_name'],
        y=df3['y'],
        opacity=.7,
        marker=dict(color=colors),
        hovertemplate='%{y:,.2f}<extra></extra>',
        showlegend=False
    )
    layout1 = go.Layout(
        title=title,
        template='seaborn',
        margin=dict(r=5, l=5, t=50, b=50),
        yaxis=yaxis,
        annotations=[
            dict(
                x=0,
                y=-0.25,
                showarrow=False,
                text="Data Source: World Bank",
                xref="paper",
                yref="paper"
            )]
    )
    data = [trace]

    return [
        {'data': data, 'layout': layout1},
        df_table.to_dict('records')
    ]
