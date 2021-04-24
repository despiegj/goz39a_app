import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from plotly.subplots import make_subplots

import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Chart
fig = make_subplots(rows=1, cols=1)
fig.add_trace(
    go.Scatter(x=np.arange(0,10,1),
               y=np.arange(0,10,1)*2 + np.random.randn(),
               name='Example'),
    row=1, col=1)
fig.update_layout(width=1500)

# Currency Options
dropdown = dcc.Dropdown(
    id='id_currency',
    options=[{"label":'Swiss Franc (CHF)','value':'CHF'},
             {"label":'Pound Sterling (GBP)','value':'GBP'},
             {"label":'Swedish Krone (SEK)','value':'SEK'},
             ],
    value='CHF')

# Start Date,  End Date & Number of Mixtures
input_groups = dbc.Row(dbc.Col(
    html.Div([
    dbc.InputGroup([
        dbc.InputGroupAddon("Start Date", addon_type="prepend"),
        dbc.Input(value="2020-01-01")],className="mb-3",),
    dbc.InputGroup([
        dbc.InputGroupAddon("End Date", addon_type="prepend"),
        dbc.Input(value="2021-01-01")],className="mb-3",),
    dbc.InputGroup([
        dbc.InputGroupAddon("Nbr Mixtures",addon_type="prepend"),
        dbc.Input(value=3,type='number')],className="mb-3"),
    dropdown]
),md=4))


app.layout = dbc.Container(
    [
        html.Div(children=[html.H1(children='Gaussian Mixtures'),
                           html.H2(children='Data Source: ECB')],
                 style={'textAlign':'center','color':'black'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(input_groups, md=5),
                dbc.Col(dcc.Graph(id="id_graph",figure=fig), md=7),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)