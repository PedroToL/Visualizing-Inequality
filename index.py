import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

from app import app
from apps import page1, page2, page3, page4

server = app.server

nav = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("By country", header=True),
                dbc.DropdownMenuItem("General Info", href="/by-country"),
                dbc.DropdownMenuItem("By Gender", href="/by-country-gender"),
                dbc.DropdownMenuItem("By Area", href="/by-country-area"),
                dbc.DropdownMenuItem("Back", href="/"),
            ],
            nav=True,
            in_navbar=True,
            label="By country",
        )
    ],
    brand="Visualizing Inequality in Latin America",
    brand_href="/",
    color="dark",
    dark=True
)
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(
            [
                html.Div(nav)
            ]
        ),
        html.Div(id='page-content')
    ]
    , id='doc')


@app.callback(
    Output('page-content', 'children'),
    [
        Input('url', 'pathname')
    ]
)
def display_page(pathanme):
    if pathanme == '/' or pathanme == '':
        return page1.layout
    if pathanme == '/by-country':
        return page2.layout
    elif pathanme == '/by-country-gender':
        return page3.layout
    elif pathanme == '/by-country-area':
        return page4.layout


if __name__ == "__main__":
    app.run_server(debug=True)
