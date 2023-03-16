import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import random

# Load the data and only randomly pick 10% of the data
random.seed(532)
data = pd.read_csv("assets/data/van_houses.csv").sample(frac=0.1)
logo = html.Img(src="assets/img/logo.png", className="header-img",
                style={'height': '10%', 'width': '10%'})
title = html.H1('Vancouver Housing Values', style={'textAlign': 'center'})

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

load_figure_template('DARKLY')

# Define the layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                logo, title
                # dbc.Col(logo, md=2),
                # dbc.Col(title, md=10)
            ],
            align='center',
            justify='center'
        ),

        dbc.Row([dbc.Col(
            [
                html.Label('Select Communities:'),
                dcc.Dropdown(
                    id='geo-dropdown',
                    options=[{'label': 'All', 'value': 'all'}] + [{'label': x, 'value': x}
                                                                  for x in sorted(list(set(data['Geo Local Area'])))],
                    value=['Downtown', 'Kerrisdale'], multi=True, placeholder='Select a community'
                ),
                html.Label('Select Built Year:'),
                dcc.RangeSlider(
                    min(data['year_built']), max(data['year_built']), 1,
                    id='yearbuilt-slider',
                    value=[min(data['year_built']), max(data['year_built'])],
                    marks=None, tooltip={"placement": "bottom", "always_visible": True})
            ], md=2),

            dbc.Col(
            [
                dcc.Graph(
                    id='map',
                    style={'display': 'inline-block', 'border-width': '0',
                           'width': '100%', }
                ),
                dcc.Graph(
                    id='piechart',
                    style={'display': 'inline-block', 'border-width': '0',
                           'width': '50%'}
                ),
                dcc.Graph(
                    id="histogram",
                    style={'display': 'inline-block', 'border-width': '0',
                           'width': '50%'}
                ),
            ], md=10),
        ],),
    ],
    style={'padding': '10px 10px'}
)

# Define callbacks

@app.callback(
    [Output('histogram', 'figure'),
     Output('map', 'figure'),
     Output('piechart', 'figure')],
    [Input('geo-dropdown', 'value'),
     Input('yearbuilt-slider', 'value')]
)
def update_graph(geo_values, yearbuilt_value):
    min_yearbuilt, max_yearbuilt = yearbuilt_value[0], yearbuilt_value[1]
    filtered_data = data.query('@min_yearbuilt <= year_built & year_built <= @max_yearbuilt')
    if not 'all' in geo_values:
        filtered_data = filtered_data.loc[(filtered_data['Geo Local Area'].isin(geo_values))]

    # Update histogram
    fig1 = px.box(filtered_data, x='zoning_classification', y='current_land_value',
                 color='zoning_classification',
                 )
    fig1.update_xaxes(title='House Type')
    fig1.update_yaxes(title='Current Land Value')
    fig1.update_layout(showlegend=False)

    # Do random sampling on the filtered_data to plot on map
    fig2 = px.scatter_mapbox(filtered_data, lat='latitude', lon='longitude', color='current_land_value',
                            hover_name='full_address', hover_data=['current_land_value'],
                            center={"lat": 49.2527, "lon": -123.120},
                            color_continuous_scale='Agsunset', range_color=[0, 5000000], zoom=11,
                            labels={"current_land_value": "Value ($)"})
    fig2.update_layout(mapbox_style="carto-positron")

    # Update pie chart
    df = filtered_data['zoning_classification'].value_counts()
    fig3 = px.pie(df, values=df.values, names=df.index, hole=.3)
    fig3.update_traces(textfont_size=15,
                      marker=dict(line=dict(color='#000000', width=1.5)))

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
