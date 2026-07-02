import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        "SpaceX Launch Records Dashboard",
        style={'textAlign': 'center'}
    ),

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[
                {'label': site, 'value': site}
                for site in spacex_df['Launch Site'].unique()
            ]
        ],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload]
    ),

    html.Br(),

    dcc.Graph(id='success-payload-scatter-chart')
])
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

        return fig

    else:

        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success Launches for site {entered_site}'
        )

        return fig
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)

def update_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome'
        )

    else:

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome for {entered_site}'
        )

    return fig
if __name__ == '__main__':
    app.run(
    host="0.0.0.0",
    port=8050,
    debug=True
)