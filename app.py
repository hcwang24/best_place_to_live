import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
data = pd.read_csv('van_houses.csv')

# Create the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Vancouver Housing Values'),
    dcc.Graph(
        id='housing-values',
        figure=px.scatter(data, x='Geo Local Area', y='current_land_value', color='zoning_classification', title='Vancouver Housing Values')
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
