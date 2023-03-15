import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import random

# Load the data
data = pd.read_csv('van_houses.csv')
logo = html.Img(src="logo.png", alt="Logo")

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

load_figure_template('DARKLY')

# Define the layout
app.layout = html.Div(
    children=[
        dbc.Row(children=[
            logo, 
            html.H1(children='Vancouver Housing Values')],
            style={'padding': '20px'}),

        dbc.Row(children=[
            dbc.Col(children=[html.Label('Select Vancouver Communities'),
                              dcc.Dropdown(
                                  id='geo-dropdown',
                                  options=[{'label': 'All', 'value': 'all'}] + [{'label': x, 'value': x}
                                                                                for x in sorted(list(set(data['Geo Local Area'])))],
                                  value=['Downtown', 'Kerrisdale'], multi=True, placeholder='Select a community'),
                              ], md=2),

            dbc.Col(
                children=[
                    dcc.Graph(
                        id='histogram',
                        style={'display': 'inline-block', 'border-width': '0',
                               'width': '45%', 'height': '500px'}
                    ),
                    dcc.Graph(
                        id='map',
                        style={'display': 'inline-block', 'border-width': '0',
                               'width': '55%', 'height': '500px'}
                    ),
                ]
            ),
        ]),  # add margin to the row
    ],
    style={'padding': '10px 10px'}
)

# Define callbacks


@app.callback(
    Output('histogram', 'figure'),
    Input('geo-dropdown', 'value')
)
def update_graph(geo_values):
    if 'all' in geo_values:
        filtered_data = data
    else:
        filtered_data = data.loc[(data['Geo Local Area'].isin(geo_values))]
    fig = px.box(filtered_data, x='zoning_classification', y='current_land_value',
                 color='zoning_classification',
                 )
    fig.update_xaxes(title='House Type')
    fig.update_yaxes(title='Current Land Value')
    fig.update_layout(showlegend=False)
    return fig


@app.callback(
    Output('map', 'figure'),
    Input('geo-dropdown', 'value')
)
def update_map(geo_values):
    random.seed(532)
    if 'all' in geo_values:
        filtered_data = data.sample(frac=0.1)
    else:
        filtered_data = data.loc[(
            data['Geo Local Area'].isin(geo_values))].sample(frac=0.1)
    fig = px.scatter_mapbox(filtered_data, lat='latitude', lon='longitude', color='current_land_value',
                            hover_name='full_address', hover_data=['current_land_value'],
                            center={"lat": 49.2527, "lon": -123.120},
                            color_continuous_scale='YlOrRd', range_color=[0, 5000000], zoom=11,
                            labels={"current_land_value": "Value ($)"})
    fig.update_layout(mapbox_style="carto-positron")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
