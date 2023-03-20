import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
import random

data = pd.read_csv("assets/data/van_houses.csv")
logo = html.Img(
    src="assets/img/logo.png",
    style={"width": "100%", "align": "center", "paddingBottom": "20px"},
)
title = html.H1(
    "Vancouver Housing App",
    style={"textAlign": "center", "fontWeight": "bold", "color": "white"},
)

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

server = app.server

load_figure_template("darkly")


# Define the layout
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        logo,
                        dbc.Row(
                            [
                                html.Label("Select Communities:"),
                                dcc.Dropdown(
                                    id="geo-dropdown",
                                    options=[{"label": "All", "value": "all"}]
                                    + [
                                        {"label": x, "value": x}
                                        for x in sorted(
                                            list(set(data["Geo Local Area"]))
                                        )
                                    ],
                                    value=["Downtown", "Kerrisdale",
                                           "Marpole", "Kitsilano"],
                                    multi=True,
                                    placeholder="Select a community",
                                ),
                                daq.BooleanSwitch(
                                    id='boolean-switch',
                                    on=True,
                                    label="Show fractioned data",
                                    labelPosition="left"
                                ),
                                html.Div(id='output'),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Warning"),
                                        dbc.ModalBody("The map on default shows 10% of the full data points. Turning the switch off will display all data and may take a long time to load."),
                                    ],
                                    id="warning-modal",
                                    centered=True,
                                    is_open=False,
                                )
                            ],
                            style={"paddingBottom": "20px"},
                        ),
                        dbc.Row(
                            [
                                html.Label("Select Property Type:"),
                                dcc.Dropdown(
                                    id="zoning-dropdown",
                                    options=[{"label": "All", "value": "all"}]
                                    + [
                                        {"label": x, "value": x}
                                        for x in sorted(
                                            list(
                                                set(data["zoning_classification"]))
                                        )
                                    ],
                                    value='all',
                                    multi=True,
                                    placeholder="Select a property type",
                                ),
                            ],
                            style={"paddingBottom": "20px"},
                        ),
                        dbc.Row(
                            [
                                html.Label("Select Built Year:"),
                                dcc.RangeSlider(
                                    min(data["year_built"]),
                                    max(data["year_built"]),
                                    1,
                                    id="yearbuilt-slider",
                                    value=[
                                        min(data["year_built"]),
                                        max(data["year_built"]),
                                    ],
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={"paddingBottom": "20px"},
                        ),
                        dbc.Row(
                            [
                                html.Label("Select Improvement Year:"),
                                dcc.RangeSlider(
                                    min(data["big_improvement_year"]),
                                    max(data["big_improvement_year"]),
                                    1,
                                    id="yearimprov-slider",
                                    value=[
                                        min(data["big_improvement_year"]),
                                        max(data["big_improvement_year"]),
                                    ],
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={"paddingBottom": "20px"},
                        ),
                    ],
                    # vertical=True,
                    # pills=True,
                    style={
                        "background-color": "rgba(248, 249, 250, 0.9)",
                        "border-right": "1px solid #dee2e6",
                        "padding": "20px",
                        "height": "95vh",
                        "width": "250px",
                        "margin": "0",
                        "opacity": "0.9",
                    },
                    md=2,
                    sm=2,
                ),
                dbc.Col(
                    [
                        # Side bar
                        # Title
                        dbc.Row(
                            title,
                            align="center",
                            justify="center",
                            style={"height": "5%"},
                        ),
                        # Graphs
                        dbc.Row(
                            dcc.Loading(
                                id="card-loading",
                                children=dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H4(
                                                "Property maps and trends"),
                                            style={'height': '10px'}
                                        ),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="map",
                                                    style={
                                                        "display": "inline-block",
                                                        "padding": "0",
                                                        "margin": "0",
                                                        "width": "50%",
                                                        "height": "325px",
                                                        "opacity": 0.9,
                                                    },
                                                ),
                                                dcc.Graph(
                                                    id="trends",
                                                    style={
                                                        "display": "inline-block",
                                                        "padding": "0",
                                                        "margin": "0",
                                                        "width": "50%",
                                                        "height": "325px",
                                                        "opacity": 0.9,
                                                    },
                                                ),
                                            ]
                                        ),
                                    ],
                                    color="rgba(0,0,0, 0.7)",
                                    inverse=True,
                                    style={'width': '100%',
                                           'margin': '0 auto', 'height': '330px'},
                                ),
                                type="circle",
                            )
                        ),
                        dbc.Row(
                            dcc.Loading(
                                id="card-loading2",
                                children=dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H4(
                                                "Property Types in Selected Region"),
                                            style={'height': '10px'}
                                        ),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="histogram",
                                                    style={
                                                        "display": "inline-block",
                                                        "padding": "0",
                                                        "margin": "0",
                                                        "width": "65%",
                                                        "height": "325px",
                                                        "opacity": 0.9,
                                                    },
                                                ),
                                                dcc.Graph(
                                                    id="piechart",
                                                    style={
                                                        "display": "inline-block",
                                                        "padding": "0",
                                                        "margin": "0",
                                                        "width": "33%",
                                                        "height": "325px",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ],
                                    color="rgba(0,0,0, 0.7)",
                                    inverse=True,
                                    style={'width': '100%',
                                           'margin': '0 auto', 'height': '330px'},
                                ),
                                type="circle",
                            )
                        ),
                    ],
                    style={
                        "padding": "10px 10px",
                    },
                    md=9,
                    sm=9,
                ),
            ]
        ),
        html.Footer(
            html.Div(
                [
                    html.P("Copyright © 2023 HanChen Wang, UBC Master of Data Science"),
                ],
            ),
        ),
    ],
    style={
        "padding": "10px",
        "background-image": 'url("assets/img/IMG_5724.png")',
        "background-size": "cover",
        "height": "100vh"
    },
)


# Define callbacks    
@app.callback(Output("warning-modal", "is_open"),
              [Input('boolean-switch', 'on')])
def toggle_warning_modal(on):
    if not on:
        return True
    return False

@ app.callback(
    [
        Output("map", "figure"),
        Output("trends", "figure"),
        Output("histogram", "figure"),
        Output("piechart", "figure"),
    ],
    [Input("boolean-switch", "on"),
     Input("geo-dropdown", "value"),
     Input("zoning-dropdown", "value"),
     Input("yearbuilt-slider", "value"),
     Input("yearimprov-slider", "value")],
)
def update_graph(on, geo_values, zoning_values, yearbuilt_value, yearimprov_value):
    min_yearbuilt, max_yearbuilt = yearbuilt_value[0], yearbuilt_value[1]
    min_yearimprov, max_yearimprov = yearimprov_value[0], yearimprov_value[1]
    filtered_data = data.query(
        "@min_yearbuilt <= year_built & year_built <= @max_yearbuilt & @min_yearimprov <= year_built & year_built <= @max_yearimprov"
    )
    if not "all" in geo_values:
        filtered_data = filtered_data.loc[
            (filtered_data["Geo Local Area"].isin(geo_values))
        ]

    if not "all" in zoning_values:
        filtered_data = filtered_data.loc[
            (filtered_data["zoning_classification"].isin(zoning_values))
        ]

    # Do random sampling on the filtered_data to plot on map
    # Load the data and only randomly pick 10% of the data
    random.seed(532)
    if not on:
        map_data = filtered_data.copy().sample(frac=0.1)
    else:
        map_data = filtered_data.copy()
    fig1 = px.scatter_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        color="current_land_value",
        hover_name="full_address",
        hover_data=["current_land_value"],
        center={"lat": 49.2527, "lon": -123.120},
        color_continuous_scale="Agsunset",
        range_color=[0, 5000000],
        zoom=10,
        labels={"current_land_value": "Value ($)"},
    )
    fig1.update_layout(
        mapbox_style="carto-positron",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Update trendline
    trend_data = pd.DataFrame(filtered_data.groupby(["Geo Local Area", "tax_assessment_year"]).mean(
        numeric_only=True)['current_land_value']).reset_index()
    trend_data['tax_assessment_year'] = trend_data['tax_assessment_year'].astype(
        int)
    fig2 = px.line(trend_data, x="tax_assessment_year",
                   y="current_land_value", color="Geo Local Area")
    # title="Average Current Land Value by Geo Local Area and Tax Assessment Year")
    fig2.update_xaxes(title="Year")
    fig2.update_yaxes(title="Value ($)")
    fig2.update_layout(xaxis={'tickmode': 'array', 'tickvals': [
                       '2020', '2021', '2022', '2023']},
                       paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)")

    # Setting color dictionary for fig3 and 4.
    color_dict = {
        "Comprehensive Development": "#1f77b4",
        "Single Detached House": "#ff7f0e",
        "Duplex": "#2ca02c",
        "One-Family Dwelling": "#d62728",
        "Two-Family Dwelling": "#9467bd",
        "Multiple Dwelling": "#8c564b",
        "Commercial": "#e377c2",
        "Industrial": "#7f7f7f",
        "Historical Area": "#bcbd22",
        "Limited Agriculture": "#17becf",
        "Other": "#ff0000"
    }

    # Update histogram
    fig3 = px.histogram(
        filtered_data.query("current_land_value <=5000000"),
        x="current_land_value",
        color="zoning_classification",
        range_x=[0, 5000000],
        nbins=20,
        color_discrete_map=color_dict,
        barmode='overlay',
    )
    fig3.update_yaxes(title="Number of properties")
    fig3.update_xaxes(title="Value ($)")
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.8)",
        legend=dict(title="Property Types", bgcolor="rgba(0,0,0,0)")
    )

    # Update pie chart
    df = filtered_data["zoning_classification"].value_counts()
    fig4 = px.pie(df, values=df.values, names=df.index, hole=0.3,
                  color=df.index, color_discrete_map=color_dict)
    fig4.update_traces(
        textfont_size=15, marker=dict(line=dict(color="#000000", width=1.5))
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                       plot_bgcolor="rgba(0,0,0,0)",
                       showlegend=False)

    return fig1, fig2, fig3, fig4


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
