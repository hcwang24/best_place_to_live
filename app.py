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
        dcc.Dropdown(
            id='geo-dropdown',
            options=[{'label': x, 'value': x} for x in sorted(list(set(data['Geo Local Area'])))],
            value='Marpole'
        )
    ], style={'padding': 10, 'flex': 1}),

    html.Div(
        children=[
            html.H1(children='Vancouver Housing Values'),
            dcc.Graph(
                id='housing-values',
                figure=px.scatter(data, x='zoning_classification', y='current_land_value',
                                  color='zoning_classification', title='Vancouver Housing Values')
            )
        ])
])

# Define callbacks
@app.callback(
    Output('housing-values', 'figure'),
    Input('geo-dropdown', 'value')
)
def update_graph(geo_value):
    filtered_data = data.loc[(data['Geo Local Area'] == geo_value)]
    fig = px.box(filtered_data, x='zoning_classification', y='current_land_value',
                      color='zoning_classification', title='Vancouver Housing Values')
    fig.update_xaxes(title='Community')
    fig.update_yaxes(title='House Value ($)')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
