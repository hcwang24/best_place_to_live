import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
data = pd.read_csv('van_houses.csv')

# Create the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children='Vancouver Housing Values'),
                html.Label('Geo Local Area'),
                dcc.Checklist(
                    id='geo-checkbox',
                    options=[{'label': x, 'value': x}
                             for x in sorted(list(set(data['Geo Local Area'])))],
                    value=['Marpole']
                )
            ],
            style={'padding': 10}
        ),

        html.Div(
            children=[
                dcc.Graph(
                    id='housing-values',
                    figure=px.box(data, x='Geo Local Area', y='current_land_value',
                                  color='zoning_classification', title='Vancouver Housing Values',
                                  boxmode='group')
                ),
                dcc.Graph(
                    id='map',
                    style={'width': '100%', 'height': '500px', 'margin': '20px 0'}
                )
            ],
            style={'display': 'flex', 'flex-direction': 'row', 'margin': '20px 0'}
        ),
    ],
    style={'padding': '20px 50px'}
)

# Define callbacks


@app.callback(
    Output('housing-values', 'figure'),
    Input('geo-checkbox', 'value')
)
def update_graph(geo_values):
    filtered_data = data.loc[(data['Geo Local Area'].isin(geo_values))]
    fig = px.box(filtered_data, x='zoning_classification', y='current_land_value',
                 color='zoning_classification', title='Vancouver Housing Values', height=500)
    fig.update_xaxes(title='House Type')
    fig.update_yaxes(title='Current Land Value')
    return fig


@app.callback(
    Output('map', 'figure'),
    Input('geo-checkbox', 'value')
)
def update_map(geo_values):
    filtered_data = data.loc[(data['Geo Local Area'].isin(geo_values))]
    fig = px.scatter_mapbox(filtered_data, lat='latitude', lon='longitude',
                            hover_name='full_address', hover_data=['current_land_value'],
                            zoom=11, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
