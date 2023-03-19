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
                style={'width': '100%', 'align': 'center', 'paddingBottom': '50px'})
title = html.H1('Vancouver Housing App', style={'textAlign': 'center', 'fontWeight': 'bold', 'color': 'white'})

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

load_figure_template('darkly')


# Define the layout
app.layout = html.Div(
    [dbc.Row([
        dbc.Col(
            [
                logo,

                dbc.Row([html.Label('Select Communities:'),
                         dcc.Dropdown(
                        id='geo-dropdown',
                        options=[{'label': 'All', 'value': 'all'}] + [{'label': x, 'value': x}
                                                                      for x in sorted(list(set(data['Geo Local Area'])))],
                        value=['Downtown', 'Kerrisdale'], multi=True, placeholder='Select a community'),
                ], style={'paddingBottom': '50px'}
                ),
                dbc.Row([
                        html.Label('Select Built Year:'),
                        dcc.RangeSlider(
                            min(data['year_built']), max(
                                data['year_built']), 1,
                            id='yearbuilt-slider',
                            value=[min(data['year_built']),
                                   max(data['year_built'])],
                            marks=None, tooltip={"placement": "bottom", "always_visible": True})
                        ], style={'paddingBottom': '50px'},
                        ),
            ],
            # vertical=True,
            # pills=True,
            style={
                'background-color': 'rgba(248, 249, 250, 0.9)',
                'border-right': '1px solid #dee2e6',
                'padding': '20px',
                'height': '100vh',
                'width': '250px',
                'margin': '0',
                'opacity': '0.9'
            },
            md=2,
        ),

        dbc.Col([
            # Side bar
            # Title
            dbc.Row(title,
                align='center',
                justify='center',
                    ),

            # Graphs
            dbc.Row(
                dbc.Card([
                    dbc.CardHeader(html.H4('The most important things')),
                    dbc.CardBody(dcc.Graph(
                        id='map',
                        style={'padding': '0', 'margin': '0',
                               'width': 'auto%', 'height': '375px', 'opacity': 0.9},
                        className="border-0 bg-transparent",
                    ),
                    ),
                ], color='rgba(0,0,0, 0.7)', inverse=True,),
            ),
            dbc.Row(
                dbc.Card([
                    dbc.CardHeader(html.H4('The most important things')),
                    dbc.CardBody([dcc.Graph(
                        id='piechart',
                        style={'display': 'inline-block', 'padding': '0', 'margin': '0',
                               'width': '50%', 'height': '285px', 'opacity': 0.9}
                    ),
                        dcc.Graph(
                        id="histogram",
                        style={'display': 'inline-block', 'padding': '0', 'margin': '0',
                               'width': '50%', 'height': '285px', 'opacity': 0.9}
                    ), ]
                    ),
                ], color='rgba(0,0,0, 0.7)', inverse=True,),
            ),
        ]),
    ])
    ],
    style={'padding': 40, 'background-image': 'url("assets/img/IMG_5724.png")', 'background-size': 'cover'}
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
    filtered_data = data.query(
        '@min_yearbuilt <= year_built & year_built <= @max_yearbuilt')
    if not 'all' in geo_values:
        filtered_data = filtered_data.loc[(
            filtered_data['Geo Local Area'].isin(geo_values))]

    # Update histogram
    fig1 = px.box(filtered_data, x='zoning_classification', y='current_land_value',
                  color='zoning_classification',
                  )
    fig1.update_xaxes(title='House Type')
    fig1.update_yaxes(title='Current Land Value')
    fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Do random sampling on the filtered_data to plot on map
    fig2 = px.scatter_mapbox(filtered_data, lat='latitude', lon='longitude', color='current_land_value',
                             hover_name='full_address', hover_data=['current_land_value'],
                             center={"lat": 49.2527, "lon": -123.120},
                             color_continuous_scale='Agsunset', range_color=[0, 5000000], zoom=10,
                             labels={"current_land_value": "Value ($)"})
    fig2.update_layout(mapbox_style="carto-positron", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    # Update pie chart
    df = filtered_data['zoning_classification'].value_counts()
    fig3 = px.pie(df, values=df.values, names=df.index, hole=.3)
    fig3.update_traces(textfont_size=15,
                       marker=dict(line=dict(color='#000000', width=1.5)))
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig1, fig2, fig3


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
