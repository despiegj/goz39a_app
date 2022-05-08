import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from plotly.subplots import make_subplots

import plotly.graph_objects as go
import numpy as np
import pandas as pd

from graphs import make_plot


app = dash.Dash(__name__,title='MDA Class 2022',external_stylesheets=[dbc.themes.BOOTSTRAP],serve_locally = False)

# add this for heroku
server = app.server

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
        dbc.Input(id='id_start_date',value="2020-01-01", type="text")],),
    dbc.InputGroup([
        dbc.Input(id='id_end_date',value="2021-01-01",type="text")]),
    dbc.InputGroup([
        dbc.Input(id='id_nbr_mixtures',value=3,type='number')]),

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
    Output('id_graph','figure'),
    [Input('id_currency', 'value'),
     Input('id_start_date','value'),
     Input('id_end_date','value'),
     Input('id_nbr_mixtures','value')
     ]
)
def update_chart(currency_value,start_date,end_date,nbr):
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except:
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(x=np.arange(0,10,1),
                       y=np.arange(0,10,1)*2 + np.random.randn(),
                       name='Example'),
            row=1, col=1)
        fig.update_layout(width=1500)
        return 'Error in Input' , fig


    if nbr is None:
        nbr = 3

    nbr = max(1,min(5,nbr))
    params = {}
    params['start_date'] = start_date
    params['end_date'] = end_date
    params['currency'] = currency_value
    params['nbr_mixtures'] = nbr
    params['periods'] = 1
    fig = make_plot(params)

    return 'Gaussian Mixtures for EUR' + currency_value + \
           ' (' + str(nbr) + ' Mixtures) ' + start_date.strftime('%Y-%m-%d') + '->' + end_date.strftime('%Y-%m-%d') , fig


if __name__ == '__main__':
    app.run_server(debug=True)