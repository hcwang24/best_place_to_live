import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
data = pd.read_csv('van_houses.csv')

# Create the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal',
                     'San Francisco'], 'Montréal'),

        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                     ['Montréal', 'San Francisco'],
                     multi=True),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['New York City', 'Montréal',
                       'San Francisco'], 'Montréal'),
    ], style={'padding': 10, 'flex': 1}),

    html.Div(
        children=[
            html.H1(children='Vancouver Housing Values'),
            dcc.Graph(
                id='housing-values',
                figure=px.scatter(data, x='Geo Local Area', y='current_land_value',
                                  color='zoning_classification', title='Vancouver Housing Values')
            )
        ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
