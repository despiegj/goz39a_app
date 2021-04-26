import dash
import dash_html_components as html


app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1(children='Gaussian Mixtures'),
                                html.H2(children='Data Source: ECB')],
                      style={'textAlign':'center',
                             'color':'blue'})
if __name__ == '__main__':
    app.run_server(debug=True)