import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
%matplotlib inline

Belgium_map = gpd.GeoDataFrame.from_file('../data/arrondissements_shape/arrondissements_shape.shp')
#All four files (.dbf, .ptj, .shp, .shx) should be in the same folder, otherwise there are errors with reading the shapefile.

heat_fr = pd.read_csv('../out/hw_freq_df.csv')
heat_intens = pd.read_csv('../out/hw_int_df.csv')

Belgium_shapes = Belgium_map[['geometry', 'INS','Name1']]
Belgium_shapes = Belgium_shapes.rename(columns ={'INS':'arron'})

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

from plotly.subplots import make_subplots

import plotly.graph_objects as go
import numpy as np
import pandas as pd

Belgium_shapes_intens = Belgium_shapes.merge(heat_intens, on='arron', suffixes=('', '_drop'))
Belgium_shapes_merge = Belgium_shapes.merge(heat_fr, on='arron', suffixes=('', '_drop'))

from pyproj import crs
geo_intens=Belgium_shapes_intens.to_crs(epsg=4326)
json_intens= geo_intens.__geo_interface__ 
geo_freq=Belgium_shapes_merge.to_crs(epsg=4326)
json_freq= geo_freq.__geo_interface__ 

pooled=pd.read_csv('../data/pooled_relationship_plot.csv')
predreg=pd.read_csv('../data/blup_fs_region.csv')
studyspe=pd.read_csv('../data/temp_preds_model_arron.csv')
predreg=predreg.rename(columns={"blup_matRRfit":"BLUP","first_stage_blup_matRRfit":"First_stage"})

from dash import Dash, dcc, html
from dash.dependencies import  Input, Output
import plotly.express as px
import plotly.graph_objs as go

colorscales = []
year={}
for i in range(len(Belgium_shapes_merge.columns[3:])):
   
    year['label'] = Belgium_shapes_merge.columns[i+3]
    year['value'] = Belgium_shapes_merge.columns[i+3]
    colorscales.append(year)
    year={}

cities=[]
city={}
for i in range(len(predreg.arron.unique())):
   
    city['label'] = predreg.arron.unique()[i]
    city['value'] = predreg.arron.unique()[i]
    cities.append(city)
    city={}

    
app = Dash(__name__)

fig4 = px.line(studyspe, x="temp", y="y",color='arron')
fig4.update_layout(title="Study Specific",title_x=0.5,
                   xaxis_title='Temperature',
                   yaxis_title='Relative Risk')

app.layout = html.Div([
    html.H2('Heatwave Analysis',style={'text-align': 'center'}),
    html.P("Select the year:"),
    dcc.Dropdown(
        id='dropdown', 
        options=colorscales,
        value='1980'
    ),
    
    dbc.Row([
    dbc.Col(dcc.Graph(id="graph"),md=5),
    dbc.Col(dcc.Graph(id="graph2"),md=5)]),
    dcc.Dropdown(
        id='dropdown2', 
        options=cities,
        value='Leuven'
    ),
    dcc.Graph(id="graph3"),
    html.Hr(),
    dcc.Graph(id="graph4",figure=fig4)
    
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def change_colorscale(scale):
    df = Belgium_shapes_merge # replace with your own data source
    fig = px.choropleth(
       df, geojson=json_freq,locations=df.index, color=scale,
    color_continuous_scale=px.colors.sequential.OrRd,hover_name='Name1',range_color=[0,8]
      )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title=f"Heatwave Weeks in <b>{scale}</b>", title_x=0.5)
    return fig

@app.callback(
    Output("graph2", "figure"), 
    Input("dropdown", "value"))
def change_colorscale2(scale):
    df = Belgium_shapes_intens # replace with your own data source
    fig2 = px.choropleth(
       df, geojson=json_intens,locations=df.index, color=scale,
    color_continuous_scale=px.colors.sequential.OrRd,hover_name='Name1',range_color=[0,5.126667]
      )
    fig2.update_geos(fitbounds="locations", visible=False)
    fig2.update_layout(title=f"Heatwave Intensity in <b>{scale}</b>", title_x=0.5)
    return fig2

@app.callback(
    Output("graph3", "figure"), 
    Input("dropdown2", "value"))
def change_city(city):
    fig = px.line(predreg[predreg.arron==city], x="blup_predvar", y=["BLUP","First_stage"])
    fig.add_trace(go.Scatter(x=pooled['predvar'],y=pooled['matRRfit'],name="Population Average"))
    fig.update_layout(title=f"<b>{city}</b>",title_x=0.5,
                   xaxis_title='Temperature',
                   yaxis_title='Relative Risk')
    fig.show()
    return fig


app.run_server(debug=True,use_reloader=False)