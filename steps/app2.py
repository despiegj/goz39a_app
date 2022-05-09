import dash
from dash import html
from dash import dcc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


app = dash.Dash(__name__,title='MDA')

fig = make_subplots(rows=1, cols=1)
fig.add_trace(
    go.Scatter(x=np.arange(0,10,1),
               y=np.arange(0,10,1)*2 + np.random.randn(),
               name='Example'),
    row=1, col=1)
fig.update_layout(margin=dict(l=1, r=1, t=1, b=1))


app.layout = html.Div(children=[
    html.Div(children=[html.H1(children='Gaussian Mixtures'),
                       html.H2(children='Data Source: ECB')],
             style={'textAlign':'center','color':'black'}),
    dcc.Graph(id='id_graph',figure=fig)])



if __name__ == '__main__':
    app.run_server(debug=True)