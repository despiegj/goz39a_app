import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

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
    options=[{"label":'CHF','value':'CHF'},
             {"label":'GBP','value':'GBP'},
             {"label":'SEK','value':'SEK'},
             ],
    value='CHF')

# Start Date,  End Date & Number of Mixtures
input_groups = dbc.Row(dbc.Col(
    html.Div([
    dbc.InputGroup([
        dbc.InputGroupAddon("T0", addon_type="prepend"),
        dbc.Input(id='id_start_date',value="2020-01-01")],className="mb-3",),
    dbc.InputGroup([
        dbc.InputGroupAddon("T1", addon_type="prepend"),
        dbc.Input(id='id_end_date',value="2021-01-01")],className="mb-3",),
    dbc.InputGroup([
        dbc.InputGroupAddon("Nbr Mixtures",addon_type="prepend"),
        dbc.Input(id='id_nbr_mixtures',value=3,type='number')],className="mb-3"),

    dropdown]
)))


app.layout = dbc.Container(
    [
        html.Div(children=[html.H1(children='Gaussian Mixtures'),
                           html.H2(children='Data Source: ECB'),
                           html.H4(children='...',id='id_title')],
                 style={'textAlign':'center','color':'black'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(input_groups, md=2),
                dbc.Col(dcc.Graph(id="id_graph",figure=fig), md=10),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('id_title','children'),
    [Input('id_currency', 'value'),
     ]
)
def update_chart(input_value):
    return 'Gaussian Mixtures for ' + input_value



if __name__ == '__main__':
    app.run_server(debug=True)